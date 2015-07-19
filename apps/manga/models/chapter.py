import uuid

from django.db import models


class Chapter(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    upload_by = models.ForeignKey("User")
    number = models.IntegerField("Capitulo #:")

    class Meta:
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"

    def __str__(self):
        pass


class ChapterPicture(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chapter = models.ForeignKey("Chapter")
    number = models.IntegerField("")

    class Meta:
        verbose_name = "ChapterPicture"
        verbose_name_plural = "ChapterPictures"

    def __str__(self):
        pass