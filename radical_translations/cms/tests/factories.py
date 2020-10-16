from factory import DjangoModelFactory, Faker, Sequence

from radical_translations.cms.models import BiographyPage, BlogIndexPage, BlogPost


class BlogIndexPageFactory(DjangoModelFactory):
    title = Faker("name")
    path = "00010009"
    depth = 2

    class Meta:
        model = BlogIndexPage
        django_get_or_create = ["title", "path", "depth"]


class BlogPostFactory(DjangoModelFactory):
    title = Faker("name")
    path = Sequence(lambda n: f"00010009000{n}")
    depth = 3

    class Meta:
        model = BlogPost
        django_get_or_create = ["title", "path", "depth"]


class BiographyPageFactory(DjangoModelFactory):
    title = Faker("name")
    path = Sequence(lambda n: f"00010009000{n}")
    depth = 3
    body = "body"

    class Meta:
        model = BiographyPage
        django_get_or_create = ["title", "path", "depth", "body"]
