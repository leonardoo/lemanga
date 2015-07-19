from __future__ import unicode_literals

from django.test import TestCase

from apps.manga.models import Manga

from ..factories.manga import MangaFactory


class MangaModelTest(TestCase):

    def test_create_manga(self):
        manga = Manga(name="test1")
        manga.save()
        self.assertEqual(manga, Manga.objects.all()[0])

    def test_string_manga(self):
        manga = MangaFactory()
        self.assertEqual(str(manga), "manga-0")
