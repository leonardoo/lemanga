import factory


class MangaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'manga.Manga'
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'manga-{}'.format(n))
