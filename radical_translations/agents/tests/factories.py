from factory import DjangoModelFactory, Faker

from radical_translations.agents.models import Organisation, Person


class OrganisationFactory(DjangoModelFactory):

    name = Faker("name")

    class Meta:
        model = Organisation
        django_get_or_create = ["name"]


class PersonFactory(DjangoModelFactory):

    name = Faker("name")

    class Meta:
        model = Person
        django_get_or_create = ["name"]
