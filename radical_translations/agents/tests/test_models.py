from collections import defaultdict

import pytest

from radical_translations.agents.models import Organisation

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures("vocabulary")
class TestOrganisation:
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

        assert Organisation.objects.count() == 3
