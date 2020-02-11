from typing import Dict, List, Optional

from controlled_vocabulary.models import (
    ControlledTerm,
    ControlledTermField,
    ControlledTermsField,
)
from controlled_vocabulary.utils import search_term_or_none
from django.db import models
from geonames_place.models import Place
from model_utils.models import TimeStampedModel
from polymorphic.models import PolymorphicModel

from radical_translations.agents.models import Agent, Organisation, Person
from radical_translations.utils.models import (
    Date,
    get_gsx_entry_value,
    get_geonames_place_from_gsx_place,
)

# These models are based on the BIBFRAME 2.0 Model
# https://www.loc.gov/bibframe/docs/bibframe2-model.html


class Title(TimeStampedModel):
    """Title information relating to a resource: work title, preferred title, instance
    title, transcribed title, translated title, variant form of title, etc."""

    main_title = models.CharField(
        max_length=768, help_text="Title being addressed. Possible title component."
    )
    subtitle = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        help_text=(
            "Word, character, or group of words and/or characters that contains the "
            "remainder of the title after the main title. Possible title component."
        ),
    )

    class Meta:
        ordering = ["main_title", "subtitle"]

    def __str__(self) -> str:
        if self.subtitle:
            return f"{self.main_title}: {self.subtitle}"

        return self.main_title


class Resource(PolymorphicModel, TimeStampedModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        help_text=(
            "Title information relating to a resource: work title, preferred title, "
            "instance title, transcribed title, translated title, variant form of "
            "title, etc."
        ),
    )
    title_variant = models.ForeignKey(
        Title,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="variants",
        help_text=(
            "Title associated with the resource that is different from the Work or "
            "Instance title (titles in another language and/or script etc.)."
        ),
    )

    languages = ControlledTermsField(
        ["iso639-2"],
        blank=True,
        help_text="Language associated with a resource or its parts.",
    )
    subjects = ControlledTermsField(
        ["fast-topic"], blank=True, help_text="Subject term(s) describing a resource",
    )

    date = models.OneToOneField(
        Date,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text=(
            "Date designation associated with a resource or element of description, "
            "such as date of title variation; year a degree was awarded; date "
            "associated with the publication, printing, distribution, issue, release "
            "or production of a resource. May be date typed."
        ),
    )
    places = models.ManyToManyField(
        Place,
        blank=True,
        help_text=(
            "Geographic location or place entity associated with a resource or element "
            "of description, such as the place associated with the publication, "
            "printing, distribution, issue, release or production of a resource, place "
            "of an event."
        ),
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text=(
            "Information, usually in textual form, on attributes of a resource or some "
            "aspect of a resource."
        ),
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title.main_title

    def get_language_names(self) -> str:
        return "; ".join([language.label for language in self.languages.all()])

    get_language_names.short_description = "Languages"  # type: ignore

    @staticmethod
    def from_gsx_entry(entry: Dict[str, Dict[str, str]]) -> Optional["Resource"]:
        """Gets or creates a new `Resource` from a Google Spreadsheet dictionary
        `entry`."""
        if not entry:
            return None

        status = get_gsx_entry_value(entry, "status")

        if not status or status.lower == "original":
            work = Work.from_gsx_entry(entry)
            instance = Instance.from_gsx_entry(entry, work=work)
        else:
            instance = Instance.from_gsx_entry(entry)

        return instance

    @staticmethod
    def languages_from_gsx_entry(
        resource: "Resource", entry: Dict[str, Dict[str, str]]
    ) -> Optional[List[Optional[ControlledTerm]]]:
        """Adds languages, from a Google Spreadsheet dictionary `entry`, to the
        `resource`."""
        if not resource or not entry:
            return None

        names = get_gsx_entry_value(entry, "language")
        if not names:
            return None

        languages = []

        for name in names.split("; "):
            name = name.split(" [")[0]
            term = search_term_or_none("iso639-2", name)
            if term:
                languages.append(term)
                resource.languages.add(term)

        return languages

    @staticmethod
    def subjects_from_gsx_entry(
        resource: "Resource", entry: Dict[str, Dict[str, str]]
    ) -> Optional[List[Optional[ControlledTerm]]]:
        """Adds subjects, from a Google Spreadsheet dictionary `entry`, to the
        `resource`."""
        if not resource or not entry:
            return None

        names = get_gsx_entry_value(entry, "genre")
        if not names:
            return None

        subjects = []

        for name in names.split("; "):
            term = search_term_or_none("fast-topic", name)
            if term:
                subjects.append(term)
                resource.subjects.add(term)

        return subjects


class Classification(TimeStampedModel):
    """System of coding and organizing materials according to their subject."""

    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="classifications"
    )

    edition = ControlledTermField(
        ["fast-topic"],
        on_delete=models.CASCADE,
        help_text=(
            "Edition of the classification scheme, such as full, abridged or a number, "
            "when a classification scheme designates editions."
        ),
    )
    source = models.ForeignKey(
        Resource,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="sources",
        help_text="Resource from which value or label came or was derived.",
    )

    def __str__(self) -> str:
        return self.edition.label

    @staticmethod
    def get_or_create(resource: Resource, term: str) -> Optional["Classification"]:
        if not resource or not term:
            return None

        if term.lower() == "original" or term.lower() == "unknown":
            return None

        term = term.replace("Translation: ", "")
        edition = search_term_or_none("fast-topic", term)

        if not edition:
            return None

        classification, _ = Classification.objects.get_or_create(
            resource=resource, edition=edition
        )

        return classification


class Contribution(TimeStampedModel):
    """Agent and role with respect to the resource being described."""

    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="contributions"
    )

    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name="contributed_to",
        help_text=(
            "Entity associated with a resource or element of description, such as the "
            "name of the entity responsible for the content or of the publication, "
            "printing, distribution, issue, release or production of a resource."
        ),
    )
    roles = ControlledTermsField(
        ["wikidata"],
        blank=True,
        help_text="Function provided by a contributor, e.g., author, illustrator, etc.",
    )

    def __str__(self) -> str:
        return f"{self.agent}: {', '.join([role.label for role in self.roles.all()])}"

    @staticmethod
    def from_gsx_entry(
        resource: Resource, entry: Dict[str, Dict[str, str]], field: str, role: str
    ) -> Optional[List[Optional["Contribution"]]]:
        """Gets or creates `Contribution` records, for the `resource`, from a Google
        Spreadsheet dictionary `entry`."""
        if not resource or not entry:
            return None

        value = get_gsx_entry_value(entry, field)
        if not value:
            return None

        if field == "authors":
            cls = Person
        elif field == "organisation":
            cls = Organisation
        else:
            cls = Agent

        contributions = []

        for name in value.split("; "):
            try:
                agent = cls.objects.get(name=name)
                contributions.append(Contribution.get_or_create(resource, agent, role))
            except cls.DoesNotExist:
                pass

        return contributions

    @staticmethod
    def get_or_create(
        resource: Resource, agent: Agent, role: str
    ) -> Optional["Contribution"]:
        if not resource or not agent:
            return None

        contribution, _ = Contribution.objects.get_or_create(
            resource=resource, agent=agent
        )

        if role:
            term = search_term_or_none("wikidata", role)
            if term:
                contribution.roles.add(term)

        return contribution


class ResourceRelationship(TimeStampedModel):
    """Any relationship between Work, Instance, and Item resources."""

    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="relationships"
    )

    relationship_type = ControlledTermField(
        ["bf-crr"],
        on_delete=models.CASCADE,
        help_text="Any relationship between Work, Instance, and Item resources.",
    )
    related_to = models.ForeignKey(
        Resource, on_delete=models.CASCADE, help_text="Related resource."
    )

    def __str__(self) -> str:
        return f"{self.resource} -> {self.relationship_type.label} -> {self.related_to}"

    @staticmethod
    def get_or_create(
        resource: Resource, relationship: str, related_to: Resource
    ) -> Optional["ResourceRelationship"]:
        if not resource or not relationship or not related_to:
            return None

        term = search_term_or_none("bf-crr", relationship)
        if not term:
            return None

        rr, _ = ResourceRelationship.objects.get_or_create(
            resource=resource, relationship_type=term, related_to=related_to
        )

        return rr


class Work(Resource):
    """The highest level of abstraction, a Work, in the BIBFRAME context, reflects the
    conceptual essence of the cataloged resource: authors, languages, and what it is
    about (subjects). """

    @staticmethod
    def from_gsx_entry(entry: Dict[str, Dict[str, str]]) -> Optional["Work"]:
        """Gets or creates a new `Work` from a Google Spreadsheet dictionary
        `entry`."""
        if not entry:
            return None

        main_title = get_gsx_entry_value(entry, "title")
        if not main_title:
            return None

        title, _ = Title.objects.get_or_create(main_title=main_title)
        work, _ = Work.objects.get_or_create(title=title)

        Contribution.from_gsx_entry(work, entry, "authors", "author")

        Resource.languages_from_gsx_entry(work, entry)

        Resource.subjects_from_gsx_entry(work, entry)

        work.save()

        return work


class Instance(Resource):
    """A Work may have one or more individual, material embodiments, for example, a
    particular published form. These are Instances of the Work. An Instance reflects
    information such as its publisher, place and date of publication, and format."""

    edition_enumeration = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="Enumeration of the edition; usually transcribed.",
    )

    @staticmethod
    def from_gsx_entry(
        entry: Dict[str, Dict[str, str]], work: Work = None
    ) -> Optional["Instance"]:
        """Gets or creates a new `Instance` from a Google Spreadsheet dictionary
        `entry`."""
        if not entry:
            return None

        title = None

        if work:
            title = work.title
        else:
            main_title = get_gsx_entry_value(entry, "title")
            if not main_title:
                return None

            title, _ = Title.objects.get_or_create(main_title=main_title)

        instance, _ = Instance.objects.get_or_create(title=title)

        Contribution.from_gsx_entry(instance, entry, "authors", "author")

        Resource.languages_from_gsx_entry(instance, entry)

        Resource.subjects_from_gsx_entry(instance, entry)

        Classification.get_or_create(instance, get_gsx_entry_value(entry, "status"))

        value = get_gsx_entry_value(entry, "editionnumber")
        if value:
            instance.edition_enumeration = value

        if work:
            ResourceRelationship.get_or_create(instance, "instance of", work)
        else:
            fields_mapping = {
                "translation of": "translationof",
                "other edition": "editionof",
                "part of": "partof",
            }

            for key in fields_mapping.keys():
                value = get_gsx_entry_value(entry, fields_mapping[key])
                if value:
                    title, _ = Title.objects.get_or_create(main_title=value)
                    work, _ = Work.objects.get_or_create(title=title)
                    ResourceRelationship.get_or_create(instance, key, work)

        value = get_gsx_entry_value(entry, "year")
        if value:
            instance.date = Date.from_date_display(value)

        value = get_gsx_entry_value(entry, "location")
        if value:
            for name in value.split("; "):
                place = get_geonames_place_from_gsx_place(name)
                if place:
                    instance.places.add(place)

        Contribution.from_gsx_entry(instance, entry, "organisation", "publisher")

        value = get_gsx_entry_value(entry, "notes")
        if value:
            instance.notes = value

        instance.save()

        return instance


class Item(Resource):
    """An item is an actual copy (physical or electronic) of an Instance. It reflects
    information such as its location (physical or virtual), shelf mark, and barcode."""

    pass
