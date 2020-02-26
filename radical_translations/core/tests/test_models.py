from collections import defaultdict
from typing import Dict

import pytest

from radical_translations.agents.models import Organisation, Person
from radical_translations.core.models import (
    Classification,
    Contribution,
    Instance,
    Item,
    Resource,
    ResourceRelationship,
    Work,
)

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures("vocabulary")
class TestClassification:
    @pytest.mark.usefixtures("resource")
    def test_get_or_create(self, resource: Resource):
        assert Classification.get_or_create(None, None) is None
        assert Classification.get_or_create(resource, None) is None
        assert Classification.get_or_create(None, "adaptation") is None
        assert Classification.get_or_create(resource, "original") is None
        assert Classification.get_or_create(resource, "unknown") is None

        classification = Classification.get_or_create(resource, "adaptation")
        assert classification is not None


@pytest.mark.usefixtures("vocabulary")
class TestContribution:
    @pytest.mark.usefixtures("entry_original", "person", "resource")
    def test_from_gsx_entry(
        self,
        resource: Resource,
        entry_original: Dict[str, Dict[str, str]],
        person: Person,
    ):
        assert Contribution.from_gsx_entry(None, None, None, None) is None
        assert Contribution.from_gsx_entry(resource, None, None, None) is None
        assert Contribution.from_gsx_entry(None, entry_original, None, None) is None

        contributions = Contribution.from_gsx_entry(
            resource, entry_original, "authors", "author"
        )
        assert contributions is not None
        assert len(contributions) == 0

        entry_original["gsx$authors"]["$t"] = person.name
        contributions = Contribution.from_gsx_entry(
            resource, entry_original, "authors", "author"
        )
        assert contributions is not None
        assert len(contributions) == 1

    @pytest.mark.usefixtures("person", "resource")
    def test_get_or_create(self, person: Person, resource: Resource):
        role = "tester"

        assert Contribution.get_or_create(None, None, None) is None
        assert Contribution.get_or_create(resource, None, None) is None
        assert Contribution.get_or_create(None, person, None) is None
        assert Contribution.get_or_create(resource, person, None) is not None

        c = Contribution.get_or_create(resource, person, role)
        assert c is not None
        assert role in c.roles.first().label.lower()


@pytest.mark.usefixtures("vocabulary")
class TestResource:
    @pytest.mark.usefixtures("entry_original", "entry_translation", "resource")
    def test_from_gsx_entry(
        self,
        entry_original: Dict[str, Dict[str, str]],
        entry_translation: Dict[str, Dict[str, str]],
        resource: Resource,
    ):
        assert Resource.from_gsx_entry(None) is None

        instance = Resource.from_gsx_entry(entry_original)
        assert instance is not None
        assert "ruines" in instance.title.main_title
        assert instance.date.date_display == "1791"
        assert "Paris" in instance.places.first().address

        instance = Instance.from_gsx_entry(entry_original, resource)
        assert instance is not None
        assert instance.title.main_title == resource.title.main_title

    @pytest.mark.usefixtures("resource")
    def test_languages_from_gsx_entry(self, resource: Resource):
        entry = defaultdict(defaultdict)
        entry["gsx$language"]["$t"] = "French [fr]"

        assert Resource.languages_from_gsx_entry(None, None) is None
        assert Resource.languages_from_gsx_entry(resource, None) is None
        assert Resource.languages_from_gsx_entry(None, entry) is None

        languages = Resource.languages_from_gsx_entry(resource, entry)
        assert languages is not None
        assert len(languages) == 1

        entry["gsx$language"]["$t"] = "French [fr]; English [en]"
        languages = Resource.languages_from_gsx_entry(resource, entry)
        assert languages is not None
        assert len(languages) == 2

    @pytest.mark.usefixtures("resource")
    def test_subjects_from_gsx_entry(self, resource: Resource):
        entry = defaultdict(defaultdict)
        entry["gsx$genre"]["$t"] = "essay"

        assert Resource.subjects_from_gsx_entry(None, None) is None
        assert Resource.subjects_from_gsx_entry(resource, None) is None
        assert Resource.subjects_from_gsx_entry(None, entry) is None

        subjects = Resource.subjects_from_gsx_entry(resource, entry)
        assert subjects is not None
        assert len(subjects) == 1

        entry["gsx$genre"]["$t"] = "essay; letter"
        subjects = Resource.subjects_from_gsx_entry(resource, entry)
        assert subjects is not None
        assert len(subjects) == 2


@pytest.mark.usefixtures("vocabulary")
class TestResourceRelationship:
    @pytest.mark.usefixtures("resource")
    def test_get_or_create(self, resource: Resource):
        assert ResourceRelationship.get_or_create(None, None, None) is None
        assert ResourceRelationship.get_or_create(resource, None, resource) is None
        assert ResourceRelationship.get_or_create(None, "instance of", None) is None
        assert (
            ResourceRelationship.get_or_create(resource, "child of", resource) is None
        )

        rr = ResourceRelationship.get_or_create(resource, "instance of", resource)
        assert rr is not None
        assert resource.relationships.count() == 1


@pytest.mark.usefixtures("vocabulary")
class TestWork:
    @pytest.mark.usefixtures("entry_original")
    def test_get_instance(self, entry_original: Dict[str, Dict[str, str]]):
        Resource.from_gsx_entry(entry_original)

        work = Work.objects.first()
        instance = work.get_instance()

        assert instance is not None
        assert instance.title == work.title

    @pytest.mark.usefixtures("person")
    def test_from_gsx_entry(self, person: Person):
        assert Work.from_gsx_entry(None) is None

        entry = defaultdict(defaultdict)
        entry["gsx$title"]["$t"] = ""
        assert Work.from_gsx_entry(entry) is None

        entry["gsx$title"]["$t"] = "Work 1"
        assert Work.from_gsx_entry(entry) is not None

        entry["gsx$authors"]["$t"] = f"{person.name}; Author 2"
        w = Work.from_gsx_entry(entry)
        assert w.contributions.first().agent.name == person.name

        entry["gsx$language"]["$t"] = f"French [fr]; English [en]"
        w = Work.from_gsx_entry(entry)
        assert "French" in w.get_language_names()

    @pytest.mark.usefixtures("entry_original")
    def test_from_instance(self, entry_original: Dict[str, Dict[str, str]]):
        assert Work.from_instance(None) is None

        entry_original["gsx$title"]["$t"] = "test_from_instance"
        instance = Instance.from_gsx_entry(entry_original, None)

        work = Work.from_instance(instance)
        assert work is not None
        assert work.title == instance.title

        assert work.contributions.count() == instance.contributions.count()
        assert work.languages.count() == instance.languages.count()
        assert work.subjects.count() == instance.subjects.count()


@pytest.mark.usefixtures("vocabulary")
class TestInstance:
    @pytest.mark.usefixtures("entry_original", "resource")
    def test_instance_of(
        self, entry_original: Dict[str, Dict[str, str]], resource: Resource
    ):
        instance = Instance.from_gsx_entry(entry_original, None)
        assert instance.instance_of() is None

        instance = Instance.from_gsx_entry(entry_original, resource)
        work = instance.instance_of()
        assert work is not None

    @pytest.mark.usefixtures(
        "entry_original",
        "entry_translation",
        "entry_edition",
        "resource",
        "organisation",
        "person",
    )
    def test_from_gsx_entry(
        self,
        entry_original: Dict[str, Dict[str, str]],
        entry_translation: Dict[str, Dict[str, str]],
        entry_edition: Dict[str, Dict[str, str]],
        resource: Resource,
        organisation: Organisation,
        person: Person,
    ):
        assert Instance.from_gsx_entry(None, None) is None

        instance = Instance.from_gsx_entry(entry_original, None)
        assert instance is not None
        assert "ruines" in instance.title.main_title
        assert instance.date.date_display == "1791"
        assert "Paris" in instance.places.first().address

        instance = Instance.from_gsx_entry(entry_original, resource)
        assert instance is not None
        assert instance.title.main_title == resource.title.main_title
        assert instance.contributions.count() == 0
        assert instance.relationships.count() == 1
        assert instance.relationships.first().relationship_type.label == "instance of"

        entry_original["gsx$authors"]["$t"] = f"{person.name}"
        instance = Instance.from_gsx_entry(entry_original, resource)
        assert instance.contributions.count() == 1

        entry_original["gsx$organisation"]["$t"] = f"{organisation.name}"
        instance = Instance.from_gsx_entry(entry_original, resource)
        assert instance.contributions.count() == 2
        assert instance.relationships.count() == 1

        instance = Instance.from_gsx_entry(entry_translation)
        assert instance.relationships.count() == 1
        assert (
            instance.relationships.first().relationship_type.label == "translation of"
        )

        instance = Instance.from_gsx_entry(entry_edition)
        assert instance.relationships.count() == 2
        assert (
            instance.relationships.first().relationship_type.label == "translation of"
        )
        assert instance.relationships.last().relationship_type.label == "other edition"


class TestItem:
    @pytest.mark.usefixtures("entry_original", "entry_edition")
    def test_from_gsx_entry(
        self,
        entry_original: Dict[str, Dict[str, str]],
        entry_edition: Dict[str, Dict[str, str]],
    ):
        assert Item.from_gsx_entry(None, None) is None
        assert Item.from_gsx_entry(entry_edition, None) is None

        instance = Instance.from_gsx_entry(entry_original, None)
        assert Item.from_gsx_entry(None, instance) is None
        assert Item.from_gsx_entry(entry_original, instance) is None

        instance = Instance.from_gsx_entry(entry_edition, None)
        item = Item.from_gsx_entry(entry_edition, instance)
        assert item is not None
        assert item.held_by.count() == 1
        assert item.electronic_locator is not None
