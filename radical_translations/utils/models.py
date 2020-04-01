import re
from typing import Dict, Optional

from django.db import models
from edtf.fields import EDTFField
from edtf.parser.edtf_exceptions import EDTFParseException
from geonames_place.models import Place
from model_utils.models import TimeStampedModel


class Date(TimeStampedModel):
    """Date designation associated with a resource or element of description, such as
    date of title variation; year a degree was awarded; date associated with the
    publication, printing, distribution, issue, release or production of a resource.
    May be date typed. Implemente using the EDTF format:
    https://github.com/ixc/python-edtf."""

    date_display = models.CharField(
        max_length=255,
        blank=True,
        help_text="Date in EDTF format: https://www.loc.gov/standards/datetime/",
    )

    date_edtf = EDTFField(
        natural_text_field="date_display",
        lower_fuzzy_field="date_earliest",
        upper_fuzzy_field="date_latest",
        lower_strict_field="date_sort_ascending",
        upper_strict_field="date_sort_descending",
        blank=True,
        null=True,
    )

    # for filtering
    date_earliest = models.FloatField(blank=True, null=True)
    date_latest = models.FloatField(blank=True, null=True)

    # for sorting
    date_sort_ascending = models.FloatField(blank=True, null=True)
    date_sort_descending = models.FloatField(blank=True, null=True)

    date_radical = models.CharField(
        max_length=255, blank=True, null=True, help_text="Alternative calendar date"
    )

    class Meta:
        ordering = ["date_sort_ascending", "date_sort_descending"]

    def __str__(self) -> str:
        if self.date_radical:
            return f"{self.date_radical} ({self.date_display})"

        return self.date_display

    @staticmethod
    def from_date_display(date_display: str) -> Optional["Date"]:
        """Create a new `Date` from a `date_display` value."""
        if not date_display:
            return None

        try:
            date = Date(date_display=date_display)
            date.save()
        # https://github.com/ixc/python-edtf/issues/32
        except (AttributeError, EDTFParseException):
            return None

        return date


def get_gsx_entry_value(entry: Dict[str, Dict[str, str]], field: str) -> Optional[str]:
    """Returns the `entry` value for the given `field`."""
    if not entry or not field:
        return None

    field = f"gsx${field}"
    if field not in entry:
        return None

    return entry[field]["$t"].strip()


GSX_PLACE = re.compile(r"\d{4}:\s(?P<address>[^\[]*)\[(?P<country_code>\w{2})\]")


def get_geonames_place_from_gsx_place(name: str) -> Optional[Place]:
    """Returns a Geonames `Place` from a Google Spreadsheet place `name`. The GSX place
    name is in the format `ID: Address [country_code]`."""
    if not name:
        return None

    matches = GSX_PLACE.match(name)
    if not matches:
        return None

    address = matches.group("address").strip()
    country_code = matches.group("country_code")

    return Place.get_or_create_from_geonames(address, country_code=country_code)
