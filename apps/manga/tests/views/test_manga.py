from __future__ import unicode_literals

from test_plus.test import TestCase

from ..factories import MangaFactory


class MangaViewsTest(TestCase):

    def setUp(self):
        MangaFactory.reset_sequence(0)
        for i in range(4):
            MangaFactory()

    def test_response200_list_view(self):
        response = self.get_check_200('list-mangas')

    def test_get_list(self):
        self.get('list-mangas')
        self.response_200()
        self.assertInContext('list')
        self.assertEqual(self.context['list'].count(), 4)

    def test_get_create(self):
        self.get('create-manga')
        self.response_200()
        self.assertInContext('form')

    def test_get_create(self):
        self.post('create-manga', follow=True, data={'name': "manga-tests"})
        self.response_200()
        self.assertInContext('list')