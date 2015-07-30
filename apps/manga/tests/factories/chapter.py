import factory

from .manga import MangaFactory
from .user import UserFactory


class ChapterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'manga.Chapter'

    number = factory.Sequence(lambda n: n)
    manga = factory.SubFactory(MangaFactory)
    upload_by = factory.SubFactory(UserFactory)

class ChapterPictureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'manga.ChapterPicture'

    number = factory.Sequence(lambda n: n)
    chapter = factory.SubFactory(ChapterFactory)
    picture = factory.django.ImageField(color='blue')