from django.db import models
from geonames_place.models import Place
from model_utils.models import TimeStampedModel

from radical_translations.core.models import Resource
from radical_translations.utils.models import (
    Date,
    get_geonames_place_from_gsx_place,
    get_gsx_entry_value,
)

# These models are based on the BIBFRAME 2.0 Event model
# http://id.loc.gov/ontologies/bibframe.html#c_Event


class Event(TimeStampedModel):
    """Something that happens at a certain time and location, such as a performance,
    speech, or athletic event, that is documented by a resource."""

    title = models.CharField(max_length=256, help_text="The title of the Event.")

    date = models.OneToOneField(
        Date,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="The date of the Event.",
    )
    place = models.ForeignKey(
        Place,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="The location the Event took place at.",
    )
    related_to = models.ManyToManyField(
        Resource,
        blank=True,
        related_name="events",
        help_text="Resources that are related to this  Event.",
    )

    class Meta:
        ordering = ["date"]

    def __str__(self) -> str:
        return f"{self.date}: {self.title}"

    @staticmethod
    def from_gsx_entry(entry: dict) -> "Event":
        """Gets or creates a new `Event` from a Google Spreadsheet dictionary
        `entry`."""
        if not entry:
            return None

        title = get_gsx_entry_value(entry, "title")
        if not title:
            return None

        date = Date.from_date_display(get_gsx_entry_value(entry, "date"))

        place = get_geonames_place_from_gsx_place(
            get_gsx_entry_value(entry, "location")
        )

        event, _ = Event.objects.get_or_create(title=title, date=date, place=place)

        return event
