import re
from typing import Dict, Optional

from controlled_vocabulary.models import ControlledTermsField
from convertdate import french_republican
from django.db import models
from edtf import parse_edtf
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
        help_text="Date in EDTF format: https://www.loc.gov/standards/datetime/",
    )
    date_display_classification = ControlledTermsField(
        ["wikidata"],
        blank=True,
        help_text="Editorial classification of the display date.",
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
        max_length=255, blank=True, null=True, help_text="Alternative calendar date."
    )
    date_radical_classification = ControlledTermsField(
        ["wikidata"],
        blank=True,
        help_text="Editorial classification of the radical date.",
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


class EditorialClassificationModel(models.Model):
    classification = ControlledTermsField(
        ["wikidata"], blank=True, help_text="Editorial classification.",
    )

    class Meta:
        abstract = True


def get_date_radical_from_gregorian(date_display: str) -> Optional[str]:
    if not date_display:
        return None

    try:
        date_edtf = parse_edtf(date_display)
        if not date_edtf:
            return None

        date_fr = french_republican.from_gregorian(*date_edtf.lower_strict()[:3])
        date_str = (
            f"{date_fr[2]} "
            f"{french_republican.MOIS[date_fr[1] - 1].lower()} "
            f"an {int(date_fr[0])}"
        )

        if date_edtf.lower_strict() != date_edtf.upper_strict():
            date_fr = french_republican.from_gregorian(*date_edtf.upper_strict()[:3])
            date_str = (
                f"{date_str} - "
                f"{date_fr[2]} "
                f"{french_republican.MOIS[date_fr[1] - 1].lower()} "
                f"an {int(date_fr[0])}"
            )

        return date_str
    except EDTFParseException:
        return None


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
