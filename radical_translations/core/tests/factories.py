from factory import DjangoModelFactory, Faker, SubFactory

from radical_translations.core.models import Resource, Title


class TitleFactory(DjangoModelFactory):
    main_title = Faker("name")

    class Meta:
        model = Title
        django_get_or_create = ["main_title"]


class ResourceFactory(DjangoModelFactory):
    title = SubFactory(TitleFactory)

    class Meta:
        model = Resource
        django_get_or_create = ["title"]
