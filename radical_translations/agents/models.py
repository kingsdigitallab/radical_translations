from typing import Dict, Optional

from django.db import models
from model_utils.models import TimeStampedModel
from polymorphic.models import PolymorphicModel

from controlled_vocabulary.models import ControlledTermsField
from controlled_vocabulary.utils import search_term_or_none
from geonames_place.models import Place
from radical_translations.utils.models import (
    Date,
    get_geonames_place_from_gsx_place,
    get_gsx_entry_value,
)

# These models are based on the BIBFRAME 2.0 Agent Model, which is based on FOAF
# http://xmlns.com/foaf/spec/#term_Agent


class Agent(PolymorphicModel, TimeStampedModel):
    """Entity having a role in a resource, such as a person or organization."""

    name = models.CharField(max_length=512, help_text="The agent name.")
    radical = models.BooleanField(
        default=False,
        help_text="Wether this person was considered a radical or not.",
    )

    based_near = models.ManyToManyField(
        Place,
        blank=True,
        related_name="agents",
        help_text=(
            "A location that something is based near, for some broadly human notion "
            "of near."
        ),
    )

    page = ControlledTermsField(
        ["viaf", "cerl"], blank=True, help_text="A page or document about this Agent."
    )

    roles = ControlledTermsField(
        ["wikidata"], blank=True, help_text="Roles performed by this Agent."
    )

    sources = models.ManyToManyField(
        "core.Resource",
        blank=True,
        related_name="agents",
        help_text="Resources that are relevant bibliographic sources.",
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text=(
            "Information, usually in textual form, on attributes of an agent or some "
            "aspect of an agent."
        ),
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"[{self.agent_type}] {self.name}"

    @property
    def agent_type(self) -> str:
        return self.polymorphic_ctype.name

    @property
    def is_organisation(self) -> bool:
        return self.agent_type == 'organisation'

    @property
    def is_person(self) -> bool:
        return self.agent_type == 'person'

    @property
    def title(self) -> str:
        return self.name

    def get_place_names(self) -> str:
        return "; ".join([place.address for place in self.based_near.all()])

    get_place_names.short_description = "Places"  # type: ignore

    def get_role_names(self):
        return "; ".join([role.label for role in self.roles.all()])

    get_role_names.short_description = "Roles"  # type: ignore


class Person(Agent):
    """The Person class represents people, whether they're alive, dead, real, or
    imaginary. The Person class is a sub-class of the Agent class, since all people
    are considered 'agents' in FOAF."""

    GENDER_CHOICES = [("f", "female"), ("m", "male"), ("u", "unknown")]

    given_name = models.CharField(
        max_length=64, blank=True, null=True, help_text="The given name of some person."
    )
    family_name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="The family name of some person.",
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        help_text="The gender of this Person.",
    )

    noble = models.BooleanField(
        default=False,
        help_text="Wether this person had a noble status at birth or not.",
    )

    main_places = models.ManyToManyField(
        Place,
        blank=True,
        related_name="agents_main_places",
        help_text=(
            "Main places this Person is associated with (places of residence, etc.)."
        ),
    )

    date_birth = models.OneToOneField(
        Date,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="person_birth",
        help_text="The date of birth of this Person.",
    )
    place_birth = models.ForeignKey(
        Place,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="births",
        help_text="The location of birth of this Person.",
    )

    date_death = models.OneToOneField(
        Date,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="person_death",
        help_text="The date of death of this Person.",
    )
    place_death = models.ForeignKey(
        Place,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="deaths",
        help_text="The location of death of this Person.",
    )

    languages = ControlledTermsField(
        ["iso639-2"],
        blank=True,
        help_text="The languages this person spoke or worked with.",
    )

    knows = models.ManyToManyField(
        "self",
        blank=True,
        help_text=(
            "A person known by this person (indicating some level of reciprocated "
            "interaction between the parties)."
        ),
    )

    class Meta:
        ordering = ["family_name", "given_name", "name"]

    def get_main_places_names(self) -> str:
        return "; ".join([place.address for place in self.main_places.all()])

    get_main_places_names.short_description = "Main places"  # type: ignore

    @staticmethod
    def from_gsx_entry(entry: Dict[str, Dict[str, str]]) -> Optional["Person"]:
        """Gets or creates a new `Person` from a Google Spreadsheet dictionary
        `entry`."""
        if not entry:
            return None

        name = get_gsx_entry_value(entry, "name")
        if not name:
            return None

        person, _ = Person.objects.get_or_create(name=name)

        # person_field: gsx_field
        fields_mapping = {
            "given_name": "firstname",
            "family_name": "lastname",
            "gender": "gender",
        }

        for key in fields_mapping.keys():
            value = get_gsx_entry_value(entry, fields_mapping[key])
            if value:
                setattr(person, key, value)

        fields_mapping = {
            "date_birth": "birth",
            "date_death": "death",
        }

        for key in fields_mapping.keys():
            value = Date.from_date_display(
                get_gsx_entry_value(entry, fields_mapping[key])
            )
            if value:
                setattr(person, key, value)

        fields_mapping = {
            "place_birth": "locationbirth",
            "place_death": "locationdeath",
        }
        for key in fields_mapping.keys():
            place_names = get_gsx_entry_value(entry, fields_mapping[key])
            if place_names:
                for name in place_names.split("; "):
                    place = get_geonames_place_from_gsx_place(name)
                    if place:
                        setattr(person, key, place)

        place_names = get_gsx_entry_value(entry, "locationsresidence")
        if place_names:
            for name in place_names.split("; "):
                place = get_geonames_place_from_gsx_place(name)
                if place:
                    person.based_near.add(place)

        occupations = get_gsx_entry_value(entry, "occupations")
        if occupations:
            for name in occupations.split("; "):
                term = search_term_or_none("wikidata", name)
                if term:
                    person.roles.add(term)

        organisations = get_gsx_entry_value(entry, "organisations")
        if organisations:
            for name in organisations.split("; "):
                try:
                    org = Organisation.objects.get(name=name)
                    person.member_of.add(org)
                except Organisation.DoesNotExist:
                    pass

        collaborators = get_gsx_entry_value(entry, "collaborators")
        if collaborators:
            for name in collaborators.split("; "):
                p, _ = Person.objects.get_or_create(name=name)
                person.knows.add(p)

        person.save()

        return person


class Organisation(Agent):
    """The Organization class represents a kind of Agent corresponding to social
    instititutions such as companies, societies etc."""

    members = models.ManyToManyField(
        Agent,
        blank=True,
        related_name="member_of",
        help_text="Members of this organisation",
    )

    @staticmethod
    def from_gsx_entry(entry: Dict[str, Dict[str, str]]) -> Optional["Organisation"]:
        """Gets or creates a new `Organisation` from a Google Spreadsheet dictionary
        `entry`."""
        if not entry:
            return None

        name = get_gsx_entry_value(entry, "organisation")
        if not name:
            return None

        org, _ = Organisation.objects.get_or_create(name=name)

        value = get_gsx_entry_value(entry, "type")
        term = search_term_or_none("wikidata", value)
        if term:
            org.roles.add(term)

        value = get_gsx_entry_value(entry, "location")
        place = get_geonames_place_from_gsx_place(value)
        if place:
            org.based_near.add(place)

        org.save()

        return org
