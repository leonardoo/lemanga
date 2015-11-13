from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Chapter(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.IntegerField("Capitulo #:")
    manga = models.ForeignKey("Manga")
    upload_by = models.ForeignKey(User)

    class Meta:
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"

    def __str__(self):
        return "{0} #{1}".format(str(self.manga), self.number)

    def get_absolute_url(self):
        return reverse_lazy('manga-chapter', args=[self.manga.slug,
                                                   self.number,
                                                   self.upload_by_id,
                                                   1])


@python_2_unicode_compatible
class ChapterPicture(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chapter = models.ForeignKey("Chapter")
    number = models.IntegerField("")
    picture = models.ImageField()

    class Meta:
        ordering = ['number']
        verbose_name = "ChapterPicture"
        verbose_name_plural = "ChapterPictures"

    def __str__(self):
        return "{0} :{1}".format(str(self.chapter), self.number)

    def get_absolute_url(self):
        return reverse_lazy('manga-chapter', args=[self.chapter.manga.slug,
                                                   self.chapter.number,
                                                   self.chapter.upload_by_id,
                                                   self.number])

    def _get_object(self, number):
        model = type(self)
        try:
            model = model.objects.select_related("chapter", "chapter__manga")
            return model.get(chapter=self.chapter,
                             number=number)
        except Exception as e:
            return None

    @property
    def next(self):
        return self._get_object(self.number+1)

    @property
    def previous(self):
        return self._get_object(self.number-1)
