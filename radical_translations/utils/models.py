from django.db import models
from edtf.fields import EDTFField
from model_utils.models import TimeStampedModel


class Date(TimeStampedModel):
    """Date designation associated with a resource or element of description, such as
    date of title variation; year a degree was awarded; date associated with the
    publication, printing, distribution, issue, release or production of a resource.
    May be date typed. Implemente using the EDTF format:
    https://github.com/ixc/python-edtf."""

    date_display = models.CharField(
        blank=True,
        max_length=255,
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

    def __str__(self) -> str:
        return self.date_display
