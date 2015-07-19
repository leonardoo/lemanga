import uuid

from django.db import models
from autoslug import AutoSlugField


class Manga(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name = "Manga"
        verbose_name_plural = "Mangas"

    def __str__(self):
        pass