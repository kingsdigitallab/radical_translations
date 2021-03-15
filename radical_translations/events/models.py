from typing import Dict, Optional

from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel

from geonames_place.models import Place
from radical_translations.core.models import Resource
from radical_translations.utils.models import (
    Date,
    EditorialClassificationModel,
    date_to_dict,
    get_geonames_place_from_gsx_place,
    get_gsx_entry_value,
    place_to_dict_value,
)

# These models are based on the BIBFRAME 2.0 Event model
# http://id.loc.gov/ontologies/bibframe.html#c_Event


class Event(TimeStampedModel, EditorialClassificationModel):
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

    def get_classification(self) -> str:
        return "; ".join([c.label for c in self.classification.all()])

    get_classification.short_description = "Classification"  # type: ignore

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            **date_to_dict(self.date),
            "place": place_to_dict_value(self.place),
            "related_to": f"{settings.EXPORT_MULTIVALUE_SEPARATOR} ".join(
                [r.to_dict_value() for r in self.related_to.all()]
            ),
        }

    @staticmethod
    def from_gsx_entry(entry: Dict[str, Dict[str, str]]) -> Optional["Event"]:
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
