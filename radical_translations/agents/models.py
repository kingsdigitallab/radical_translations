from controlled_vocabulary.models import ControlledTermsField
from django.db import models
from geonames_place.models import Place
from model_utils.models import TimeStampedModel
from polymorphic.models import PolymorphicModel

from radical_translations.utils.models import (
    Date,
    get_controlled_vocabulary_term,
    get_geonames_place_from_gsx_place,
    get_gsx_entry_value,
)

# These models are based on the BIBFRAME 2.0 Agent Model, which is based on FOAF
# http://xmlns.com/foaf/spec/#term_Agent


class Agent(PolymorphicModel, TimeStampedModel):
    """Entity having a role in a resource, such as a person or organization."""

    name = models.CharField(max_length=128, help_text="The agent name.")

    based_near = models.ManyToManyField(
        Place,
        blank=True,
        help_text=(
            "A location that something is based near, for some broadly human notion "
            "of near."
        ),
    )

    page = ControlledTermsField(
        ["viaf"], blank=True, help_text="A page or document about this Agent."
    )

    roles = ControlledTermsField(
        ["wikidata"], blank=True, help_text="Roles performed by this Agent."
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


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

    date_birth = models.OneToOneField(
        Date,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="person_birth",
        help_text="The date of birth of this Person.",
    )
    date_death = models.OneToOneField(
        Date,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="person_death",
        help_text="The date of death of this Person.",
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

    @staticmethod
    def from_gsx_entry(entry: dict) -> "Person":
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

        place_fields = ["locationbirth", "locationsresidence", "locationdeath"]
        for field in place_fields:
            place_names = get_gsx_entry_value(entry, field)
            if place_names:
                for name in place_names.split("; "):
                    place = get_geonames_place_from_gsx_place(name)
                    if place:
                        person.based_near.add(place)

        occupations = get_gsx_entry_value(entry, "occupations")
        if occupations:
            for name in occupations.split("; "):
                term = get_controlled_vocabulary_term("wikidata", name)
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
    def from_gsx_entry(entry: dict) -> "Organisation":
        """Gets or creates a new `Organisation` from a Google Spreadsheet dictionary
        `entry`."""
        if not entry:
            return None

        name = get_gsx_entry_value(entry, "organisation")
        if not name:
            return None

        org = Organisation.objects.create(name=name)

        value = get_gsx_entry_value(entry, "type")
        term = get_controlled_vocabulary_term("wikidata", value)
        if term:
            org.roles.add(term)

        value = get_gsx_entry_value(entry, "location")
        place = get_geonames_place_from_gsx_place(value)
        if place:
            org.based_near.add(place)

        org.save()

        return org
