import os
import errno

from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.staticfiles.finders import BaseFinder
from django.contrib.staticfiles import utils
from django.contrib.staticfiles.utils import check_settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files import File, locks
from django.core.files.move import file_move_safe
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.utils.encoding import filepath_to_uri

from pipeline.storage import PipelineMixin

searched_locations = []


@deconstructible
class FileSystemStorage(Storage):
    """
    Standard filesystem storage
    """

    def __init__(self, location=None, base_url=None, file_permissions_mode=None,
            directory_permissions_mode=None):
        if location is None:
            location = settings.MEDIA_ROOT
        self.base_location = Path(location)
        self.location = self.base_location.absolute()
        if base_url is None:
            base_url = settings.MEDIA_URL
        elif not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url
        self.file_permissions_mode = (
            file_permissions_mode if file_permissions_mode is not None
            else settings.FILE_UPLOAD_PERMISSIONS
        )
        self.directory_permissions_mode = (
            directory_permissions_mode if directory_permissions_mode is not None
            else settings.FILE_UPLOAD_DIRECTORY_PERMISSIONS
        )

    def _open(self, name, mode='rb'):
        return File(self.path(name).open(mode))

    def _save(self, name, content):
        full_path = self.path(name)

        # Create any intermediate directories that do not exist.
        # Note that there is a race between os.path.exists and os.makedirs:
        # if os.makedirs fails with EEXIST, the directory was created
        # concurrently, and we can continue normally. Refs #16082.
        #directory = os.path.dirname(full_path)
        directory = full_path.parent
        if not directory.exists():
            try:
                if self.directory_permissions_mode is not None:
                    # os.makedirs applies the global umask, so we reset it,
                    # for consistency with file_permissions_mode behavior.
                    old_umask = os.umask(0)
                    try:
                        directory.mkdir(self.directory_permissions_mode)
                    finally:
                        os.umask(old_umask)
                else:
                    directory.mkdir()
                    #os.makedirs(directory)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        if not directory.is_dir():
            raise IOError("%s exists and is not a directory." % directory)

        # There's a potential race condition between get_available_name and
        # saving the file; it's possible that two threads might return the
        # same name, at which point all sorts of fun happens. So we need to
        # try to create the file, but if it already exists we have to go back
        # to get_available_name() and try again.

        while True:
            try:
                # This file has a file path that we can move.
                if hasattr(content, 'temporary_file_path'):
                    file_move_safe(content.temporary_file_path(), str(full_path))

                # This is a normal uploadedfile that we can stream.
                else:
                    # This fun binary flag incantation makes os.open throw an
                    # OSError if the file already exists before we open it.
                    flags = (os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                             getattr(os, 'O_BINARY', 0))
                    # The current umask value is masked out by os.open!
                    fd = os.open(str(full_path), flags, 0o666)
                    _file = None
                    try:
                        locks.lock(fd, locks.LOCK_EX)
                        for chunk in content.chunks():
                            if _file is None:
                                mode = 'wb' if isinstance(chunk, bytes) else 'wt'
                                _file = os.fdopen(fd, mode)
                            _file.write(chunk)
                    finally:
                        locks.unlock(fd)
                        if _file is not None:
                            _file.close()
                        else:
                            os.close(fd)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    # Ooops, the file exists. We need a new file name.
                    name = self.get_available_name(name)
                    full_path = self.path(name)
                else:
                    raise
            else:
                # OK, the file save worked. Break out of the loop.
                break

        if self.file_permissions_mode is not None:
            os.chmod(str(full_path), self.file_permissions_mode)

        return name

    def delete(self, name):
        assert name, "The name argument is not allowed to be empty."
        path = self.path(name)
        # If the file exists, delete it from the filesystem.
        # Note that there is a race between os.path.exists and os.remove:
        # if os.remove fails with ENOENT, the file was removed
        # concurrently, and we can continue normally.
        if path.exists():
            try:
                os.remove(name)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise

    def exists(self, name):
        return self.location.joinpath(name).exists()

    def listdir(self, path):
        path = self.path(path)
        directories, files = [], []
        for entry in path.iterdir():
            if entry.is_dir():
                directories.append(entry)
            else:
                files.append(entry)
        return directories, files

    def path(self, name):
        return self.location.joinpath(name)

    def size(self, name):
        return os.path.getsize(str(self.path(name)))

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        return urljoin(self.base_url, filepath_to_uri(name))

    def accessed_time(self, name):
        return datetime.fromtimestamp(os.path.getatime(self.path(name)))

    def created_time(self, name):
        return datetime.fromtimestamp(os.path.getctime(self.path(name)))

    def modified_time(self, name):
        return datetime.fromtimestamp(os.path.getmtime(self.path(name)))


@deconstructible
class FileSystemFinder(BaseFinder):
    """
    A static files finder that uses the ``STATICFILES_DIRS`` setting
    to locate files.
    """
    def __init__(self, app_names=None, *args, **kwargs):
        # List of locations with static files
        self.locations = []
        # Maps dir paths to an appropriate storage instance
        self.storages = OrderedDict()
        if not isinstance(settings.STATICFILES_DIRS, (list, tuple)):
            raise ImproperlyConfigured(
                "Your STATICFILES_DIRS setting is not a tuple or list; "
                "perhaps you forgot a trailing comma?")
        for root in settings.STATICFILES_DIRS:
            if isinstance(root, (list, tuple)):
                prefix, root = root
            else:
                prefix = ''
            if settings.STATIC_ROOT and os.path.abspath(settings.STATIC_ROOT) == os.path.abspath(root):
                raise ImproperlyConfigured(
                    "The STATICFILES_DIRS setting should "
                    "not contain the STATIC_ROOT setting")
            if (prefix, root) not in self.locations:
                self.locations.append((prefix, root))
        for prefix, root in self.locations:
            filesystem_storage = FileSystemStorage(location=root)
            filesystem_storage.prefix = prefix
            self.storages[root] = filesystem_storage
        super(FileSystemFinder, self).__init__(*args, **kwargs)

    def find(self, path, all=False):
        """
        Looks for files in the extra locations
        as defined in ``STATICFILES_DIRS``.
        """
        matches = []
        for prefix, root in self.locations:
            if root not in searched_locations:
                searched_locations.append(root)
            matched_path = self.find_location(root, path, prefix)
            if matched_path:
                if not all:
                    return matched_path
                matches.append(matched_path)
        return matches

    def find_location(self, root, path, prefix=None):
        """
        Finds a requested static file in a location, returning the found
        absolute path (or ``None`` if no match).
        """
        if prefix:
            prefix = '%s%s' % (prefix, os.sep)
            if not path.startswith(prefix):
                return None
            path = path[len(prefix):]
        lpath = self.storages.get(root)
        lpath = lpath.path(path)
        if lpath.exists():
            return str(lpath)

    def list(self, ignore_patterns):
        """
        List all files in all locations.
        """
        for prefix, root in self.locations:
            storage = self.storages[root]
            for path in utils.get_files(storage, ignore_patterns):
                yield path, storage


class StaticFilesStorage(FileSystemFinder):

    """
    Standard file system storage for static files.

    The defaults for ``location`` and ``base_url`` are
    ``STATIC_ROOT`` and ``STATIC_URL``.
    """
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if base_url is None:
            base_url = settings.STATIC_URL
        check_settings(base_url)
        self.base_url = base_url
        super(StaticFilesStorage, self).__init__(*args, **kwargs)

    def listdir(self, path):
        paths = self.find(path)
        directories, files = [], []
        for path in paths:
            for entry in path.iterdir():
                if entry.is_dir():
                    directories.append(entry)
                else:
                    files.append(str(entry.relative_to(path)))
        return directories, files

    def find(self, path, all=False):
        """
        Looks for files in the extra locations
        as defined in ``STATICFILES_DIRS``.
        """
        matches = []
        for prefix, root in self.locations:

            if root not in searched_locations:
                searched_locations.append(root)
            matched_path = self.find_location(root, path, prefix)
            matched_path = Path(matched_path)
            if matched_path:
                if not all:
                    return [matched_path]
                matches.append(matched_path)
        return matches

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        return urljoin(self.base_url, filepath_to_uri(name))

    def open(self, file):
        matched_path = None
        root = None
        for prefix, root in self.locations:
            matched_path = self.find_location(root, file, prefix)
            if matched_path:
                break
        if matched_path:
            return self.storages.get(root).open(file)
        return None


class PipelineStorage(PipelineMixin, StaticFilesStorage):
    pass
