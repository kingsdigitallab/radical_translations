import re
from datetime import date
from time import mktime, struct_time
from typing import Dict, Optional

from convertdate import french_republican
from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel

from controlled_vocabulary.models import ControlledTermsField
from edtf import parse_edtf
from edtf.fields import EDTFField
from edtf.parser.edtf_exceptions import EDTFParseException
from geonames_place.models import Place


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
        ordering = ["date_sort_ascending"]

    def __str__(self) -> str:
        if self.date_radical:
            return f"{self.date_radical} ({self.date_display})"

        return self.date_display

    @property
    def is_radical(self) -> bool:
        return self.date_radical is not None

    def get_date_earliest(self) -> Optional[date]:
        struct = self.parse_date()
        if not struct:
            return None

        return date.fromtimestamp(mktime(struct.lower_strict()))

    def parse_date(self) -> Optional[struct_time]:
        try:
            return parse_edtf(self.date_display)
        except (AttributeError, EDTFParseException):
            return None

    def get_date_latest(self) -> Optional[date]:
        struct = self.parse_date()
        if not struct:
            return None

        return date.fromtimestamp(mktime(struct.upper_strict()))

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


def date_to_dict(date: Date, label: Optional[str] = "date") -> Dict:
    if not date:
        return {
            f"{label}.date_display": "",
            f"{label}.date_display_classification": "",
            f"{label}.date_radical": "",
            f"{label}.date_radical_classification": "",
        }

    return {
        f"{label}.date_display": date.date_display,
        f"{label}.date_display_classification": get_controlled_terms_str(
            date.date_display_classification.all()
        ),
        f"{label}.date_radical": date.date_radical,
        f"{label}.date_radical_classification": get_controlled_terms_str(
            date.date_radical_classification.all()
        ),
    }


class EditorialClassificationModel(models.Model):
    classification = ControlledTermsField(
        ["wikidata"],
        blank=True,
        help_text="Editorial classification.",
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


def get_controlled_terms_str(terms) -> str:
    return f"{settings.EXPORT_MULTIVALUE_SEPARATOR} ".join(
        [f"{ct.label} ({ct.vocabulary.label})" for ct in terms]
    )


def place_to_dict(place) -> Dict:
    if not place:
        return

    return {
        "geonames_id": place.geonames_id,
        "address": place.address,
        "class_description": place.class_description,
        "country": place.country.name if place.country else "",
        "feature_class": place.feature_class,
        "lat": place.lat,
        "lon": place.lon,
    }


def place_to_dict_value(place) -> str:
    if not place:
        return

    if place.country:
        return (
            f"{place.geonames_id}{settings.EXPORT_FIELD_SEPARATOR}{place.address}"
            f"{settings.EXPORT_FIELD_SEPARATOR}{place.country.name}"
        )

    return place.address
