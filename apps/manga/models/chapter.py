from __future__ import unicode_literals

import uuid

from django.db import models
from django.contrib.auth.models import User
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

    @models.permalink
    def get_absolute_url(self):
        return reverse_lazy('manga_chapter', args=[self.manga.slug,
                                                   self.number,
                                                   self.user])


@python_2_unicode_compatible
class ChapterPicture(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chapter = models.ForeignKey("Chapter")
    number = models.IntegerField("")
    picture = models.ImageField()

    class Meta:
        verbose_name = "ChapterPicture"
        verbose_name_plural = "ChapterPictures"

    def __str__(self):
        return "{0} :{1}".format(str(self.chapter), self.number)
