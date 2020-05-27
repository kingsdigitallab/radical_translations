from collections import defaultdict
from typing import Dict

import pytest

from radical_translations.agents.models import Organisation, Person
from radical_translations.core.models import (
    Classification,
    Contribution,
    Resource,
    ResourceRelationship,
    Title,
)

pytestmark = pytest.mark.django_db


class TestTitle:
    def test___str__(self):
        t = Title(main_title="main")
        assert "main" in str(t)
        assert ":" not in str(t)

        t = Title(main_title="main", subtitle="sub")
        assert "main" in str(t)
        assert ":" in str(t)
        assert "sub" in str(t)

    def test_get_or_create(self):
        assert Title.get_or_create(None, None) is None

        mt = "hello"
        title = Title.get_or_create(mt)
        assert title is not None
        assert mt == title.main_title

        for mt in ["untitled", "translation"]:
            title = Title.get_or_create(mt)
            assert title is not None
            assert mt == title.main_title
            assert 1 == title.subtitle

            title = Title.get_or_create(mt)
            assert title is not None
            assert mt == title.main_title
            assert 2 == title.subtitle


@pytest.mark.usefixtures("vocabulary")
class TestClassification:
    @pytest.mark.usefixtures("resource")
    def test_get_or_create(self, resource: Resource):
        assert Classification.get_or_create(None, None) is None
        assert Classification.get_or_create(resource, None) is None
        assert Classification.get_or_create(None, "adapted") is None

        assert Classification.get_or_create(resource, "original") is not None
        assert Classification.get_or_create(resource, "unknown") is not None
        assert Classification.get_or_create(resource, "adapted") is not None


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
        assert len(contributions) == 1

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
        assert (
            Contribution.get_or_create(resource, person, None, "Pseudo Nym") is not None
        )

        c = Contribution.get_or_create(resource, person, role)
        assert c is not None
        assert role in c.roles.first().label.lower()

    @pytest.mark.usefixtures("person", "resource")
    def test___str__(self, person: Person, resource: Resource):
        c = Contribution.get_or_create(resource, person, None, None)
        assert person.name in str(c)

        pseudonym = "Pseudo Nym"

        c = Contribution.get_or_create(resource, person, None, pseudonym)
        assert pseudonym in str(c)
        assert person.name in str(c)


@pytest.mark.usefixtures("vocabulary")
class TestResource:
    @pytest.mark.usefixtures("entry_original", "entry_translation")
    def test_is_original(self, entry_original, entry_translation):
        resource = Resource.from_gsx_entry(entry_original)
        assert resource.is_original() is True

        resource = Resource.from_gsx_entry(entry_translation)
        assert resource.is_original() is False

    @pytest.mark.usefixtures("entry_original")
    def test_is_paratext(self, entry_original):
        resource = Resource.from_gsx_entry(entry_original)
        assert resource.is_paratext() is False

        paratext = Resource.paratext_from_gsx_entry(entry_original, resource)
        assert paratext.is_paratext() is True

    @pytest.mark.usefixtures("entry_original", "entry_edition")
    def test_get_authors(self, entry_original, entry_edition):
        resource = Resource.from_gsx_entry(entry_original)
        assert "Constantin" in resource.get_authors()

        resource = Resource.from_gsx_entry(entry_edition)
        authors = resource.get_authors()
        assert "Samson" in authors
        assert ";" in authors
        assert "Dalila" in authors

    @pytest.mark.usefixtures("entry_original", "entry_translation")
    def test_get_classification_edition(self, entry_original, entry_translation):
        resource = Resource.from_gsx_entry(entry_original)
        assert resource.get_classification_edition().lower() == "original"

        resource = Resource.from_gsx_entry(entry_translation)
        assert resource.get_classification_edition().lower() == "integral"

    @pytest.mark.usefixtures("entry_original", "entry_translation")
    def test_get_language_names(self, entry_original, entry_translation):
        resource = Resource.from_gsx_entry(entry_original)
        assert resource.get_language_names() == "French"

        resource = Resource.from_gsx_entry(entry_translation)
        assert resource.get_language_names() == "English"

    @pytest.mark.usefixtures("entry_original", "entry_translation")
    def test_get_place_names(self, entry_original, entry_translation):
        resource = Resource.from_gsx_entry(entry_original)
        assert resource.get_place_names() == "Paris"

        resource = Resource.from_gsx_entry(entry_translation)
        assert resource.get_place_names() == "London"

    @pytest.mark.usefixtures(
        "entry_original",
        "entry_translation",
        "entry_edition",
        "organisation",
        "person",
    )
    def test_from_gsx_entry(
        self,
        entry_original: Dict[str, Dict[str, str]],
        entry_translation: Dict[str, Dict[str, str]],
        entry_edition: Dict[str, Dict[str, str]],
        organisation: Organisation,
        person: Person,
    ):
        assert Resource.from_gsx_entry(None) is None

        entry = defaultdict(defaultdict)
        entry["gsx$title"]["$t"] = ""
        assert Resource.from_gsx_entry(entry) is None

        entry["gsx$title"]["$t"] = "Work 1"
        assert Resource.from_gsx_entry(entry) is not None

        entry["gsx$authors"]["$t"] = f"{person.name}; Author 2"
        resource = Resource.from_gsx_entry(entry)
        assert resource.contributions.first().agent.name == person.name

        entry["gsx$language"]["$t"] = f"French [fr]; English [en]"
        resource = Resource.from_gsx_entry(entry)
        assert "French" in resource.get_language_names()

        entry_original["gsx$authors"]["$t"] = ""
        entry_original["gsx$organisation"]["$t"] = ""

        resource = Resource.from_gsx_entry(entry_original)
        assert resource is not None
        assert "ruines" in resource.title.main_title
        assert resource.date.date_display == "1791"
        assert "Paris" in resource.places.first().place.address

        entry_original["gsx$authors"]["$t"] = f"{person.name}"
        resource = Resource.from_gsx_entry(entry_original)
        assert resource.contributions.count() == 1

        entry_original["gsx$organisation"]["$t"] = f"{organisation.name}"
        resource = Resource.from_gsx_entry(entry_original)
        assert resource.contributions.count() == 2

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

    @pytest.mark.usefixtures("entry_original", "resource")
    def test_paratext_from_gsx_entry(
        self, entry_original: Dict[str, Dict[str, str]], resource: Resource,
    ):
        assert Resource.paratext_from_gsx_entry(None, None) is None
        assert Resource.paratext_from_gsx_entry(entry_original, None) is None
        assert Resource.paratext_from_gsx_entry(None, resource) is None

        paratext = Resource.paratext_from_gsx_entry(entry_original, resource)
        assert paratext is not None
        assert paratext.title == resource.title
        assert paratext.summary is not None
        assert paratext.notes is not None
        assert paratext.relationships.count() == 1

    @pytest.mark.usefixtures(
        "entry_original", "entry_translation", "entry_edition"
    )
    def test_relationships_from_gsx_entry(
        self,
        entry_original: Dict[str, Dict[str, str]],
        entry_translation: Dict[str, Dict[str, str]],
        entry_edition: Dict[str, Dict[str, str]],
    ):
        assert Resource.relationships_from_gsx_entry(None) is None

        Resource.from_gsx_entry(entry_original)
        resource = Resource.relationships_from_gsx_entry(entry_original)
        assert resource is not None
        assert resource.relationships.count() == 0

        Resource.from_gsx_entry(entry_translation)
        resource = Resource.relationships_from_gsx_entry(entry_translation)
        assert resource is not None
        assert resource.relationships.count() == 1

        entry = defaultdict(defaultdict)
        entry["gsx$title"]["$t"] = "Discours sur le gouvernement"
        Resource.from_gsx_entry(entry)
        entry = defaultdict(defaultdict)
        entry["gsx$title"]["$t"] = "Discourses concerning government"
        Resource.from_gsx_entry(entry)

        Resource.from_gsx_entry(entry_edition)
        resource = Resource.relationships_from_gsx_entry(entry_edition)
        assert resource is not None
        assert resource.relationships.count() == 2


@pytest.mark.usefixtures("vocabulary")
class TestResourceRelationship:
    @pytest.mark.usefixtures("resource")
    def test_get_or_create(self, resource: Resource):
        assert ResourceRelationship.get_or_create(None, None, None) is None
        assert ResourceRelationship.get_or_create(resource, None, resource) is None
        assert (
            ResourceRelationship.get_or_create(resource, "child of", resource) is None
        )

        rr = ResourceRelationship.get_or_create(resource, "related to", resource)
        assert rr is not None
        assert resource.relationships.count() == 1
