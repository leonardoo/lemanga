from __future__ import unicode_literals

from django.test import TestCase

from apps.manga.models import Chapter, ChapterPicture

from ..factories import MangaFactory, UserFactory, ChapterFactory, ChapterPictureFactory


class ChapterModelTest(TestCase):

    def setUp(self):
        MangaFactory.reset_sequence(0)
        UserFactory.reset_sequence(0)

    def test_create_chapter(self):
        manga = MangaFactory()
        user = UserFactory()
        chapter = Chapter(number=1, manga=manga, upload_by=user)
        chapter.save()
        self.assertEqual(chapter, Chapter.objects.all()[0])

    def test_string_manga(self):
        chapter = ChapterFactory()
        self.assertEqual(str(chapter), "{0} #0".format(str(chapter.manga)))


class ChapterPictureModelTest(TestCase):

    def setUp(self):
        MangaFactory.reset_sequence(0)
        UserFactory.reset_sequence(0)

    def test_create_chapter_pictures(self):
        manga = MangaFactory()
        user = UserFactory()
        chapter = ChapterFactory()
        for i in range(4):
            ChapterPictureFactory(chapter=chapter)
        self.assertEqual(4, ChapterPicture.objects.all().count())
        chapter_image = ChapterPicture.objects.last()
        self.assertEqual(chapter, chapter_image.chapter)
