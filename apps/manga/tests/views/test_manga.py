from __future__ import unicode_literals

from test_plus.test import TestCase


class MangaModelTest(TestCase):

    def test_response200_list_view(self):
        response = self.get_check_200('list-mangas')
