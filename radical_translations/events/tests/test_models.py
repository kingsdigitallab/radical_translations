from collections import defaultdict

import pytest

from radical_translations.events.models import Event

pytestmark = pytest.mark.django_db


class TestEvent:
    def test_from_gsx_entry(self):
        assert Event.from_gsx_entry(None) is None

        entry = defaultdict(defaultdict)
        entry["gsx$title"]["$t"] = ""
        assert Event.from_gsx_entry(entry) is None

        entry["gsx$title"]["$t"] = "Event 1 title"
        assert Event.from_gsx_entry(entry) is not None

        entry["gsx$date"]["$t"] = "1979?"
        assert Event.from_gsx_entry(entry) is not None

        entry["gsx$location"]["$t"] = "0001: London [UK]"
        assert Event.from_gsx_entry(entry) is not None
