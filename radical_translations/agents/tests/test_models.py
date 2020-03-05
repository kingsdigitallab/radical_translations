from collections import defaultdict

import pytest

from radical_translations.agents.models import Organisation, Person

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures("vocabulary")
class TestOrganisation:
    def test_agent_type(self, title):
        obj = Person(name="person name")
        obj.save()
        assert obj.agent_type == "person"

        obj = Organisation(name="organisation name")
        obj.save()
        assert obj.agent_type == "organisation"

    def test_from_gsx_entry(self):
        assert Organisation.from_gsx_entry(None) is None

        entry = defaultdict(defaultdict)
        entry["gsx$organisation"]["$t"] = ""
        assert Organisation.from_gsx_entry(entry) is None

        entry["gsx$organisation"]["$t"] = "Organisation 1"
        assert Organisation.from_gsx_entry(entry) is not None

        entry["gsx$type"]["$t"] = "Publisher"
        assert Organisation.from_gsx_entry(entry) is not None

        entry["gsx$location"]["$t"] = "0001: London [UK]"
        assert Organisation.from_gsx_entry(entry) is not None

        assert Organisation.objects.count() == 1


@pytest.mark.usefixtures("vocabulary")
class TestPerson:
    def test_from_gsx_entry(self):
        assert Person.from_gsx_entry(None) is None

        entry = defaultdict(defaultdict)
        entry["gsx$name"]["$t"] = ""
        assert Person.from_gsx_entry(entry) is None

        entry["gsx$name"]["$t"] = "Person 1"
        assert Person.from_gsx_entry(entry) is not None

        entry["gsx$gender"]["$t"] = "f"
        p = Person.from_gsx_entry(entry)
        assert p is not None
        assert p.gender == "f"

        entry["gsx$birth"]["$t"] = "1790"
        p = Person.from_gsx_entry(entry)
        assert p is not None
        assert p.date_birth.date_display == "1790"

        entry["gsx$locationsresidence"]["$t"] = "0001: London [UK]; 0002: Paris [FR]"
        p = Person.from_gsx_entry(entry)
        assert p is not None
        assert "London" in p.based_near.first().address
        assert "Paris" in p.based_near.last().address

        entry["gsx$locationbirth"]["$t"] = "0001: London [UK]"
        p = Person.from_gsx_entry(entry)
        assert p is not None
        assert "London" in p.place_birth.address

        entry["gsx$locationdeath"]["$t"] = "0002: Paris [FR]"
        p = Person.from_gsx_entry(entry)
        assert p is not None
        assert "Paris" in p.place_death.address

        entry["gsx$occupations"]["$t"] = "tester"
        p = Person.from_gsx_entry(entry)
        assert p is not None
        assert "tester" in p.roles.first().label.lower()

        entry["gsx$organisations"]["$t"] = "Organisation 1"
        p = Person.from_gsx_entry(entry)
        assert p is not None

        entry["gsx$collaborators"]["$t"] = "Person 2; Person 3"
        p = Person.from_gsx_entry(entry)
        assert p is not None

        assert Person.objects.count() == 3
