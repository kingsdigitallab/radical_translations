import pytest

from radical_translations.utils.models import (
    Date,
    get_geonames_place_from_gsx_place,
    get_gsx_entry_value,
)

pytestmark = pytest.mark.django_db


class TestDate:
    def test_from_date_display(self):
        assert Date.from_date_display(None) is None

        date = Date.from_date_display("1971")
        assert date is not None
        assert date.date_edtf is not None


def test_get_gsx_entry_value():
    expected = "place"
    entry = {"gsx$location": {"$t": expected}}
    field = "location"

    assert get_gsx_entry_value(None, None) is None
    assert get_gsx_entry_value(entry, None) is None
    assert get_gsx_entry_value(None, field) is None
    assert get_gsx_entry_value(entry, "field") is None

    value = get_gsx_entry_value(entry, field)
    assert value is not None
    assert value == expected


def test_get_place_from_gsx_place():
    address = "London"
    name = f"0001: {address} [UK]"

    assert get_geonames_place_from_gsx_place(None) is None
    assert get_geonames_place_from_gsx_place(name[:-2]) is None

    place = get_geonames_place_from_gsx_place(name)
    assert place is not None
    assert address in place.address
