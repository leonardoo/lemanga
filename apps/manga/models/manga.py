from __future__ import unicode_literals

import uuid

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from autoslug import AutoSlugField


@python_2_unicode_compatible
class Manga(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name = "Manga"
        verbose_name_plural = "Mangas"

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return reverse_lazy('detail-manga', args=[self.slug])
