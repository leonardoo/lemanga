import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"

    username = factory.Sequence(lambda n: "Agent {0}".format(str(n)))
    email = factory.Sequence(lambda n: "{0}@1.com".format(str(n)))
    password = 'adm1n'
    is_active = True
