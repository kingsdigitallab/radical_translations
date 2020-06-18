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

from radical_translations.agents.models import Agent, Organisation, Person
from radical_translations.utils.models import (
    Date,
    EditorialClassificationModel,
    get_geonames_place_from_gsx_place,
    get_gsx_entry_value,
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
        default="",
        help_text=(
            "Word, character, or group of words and/or characters that contains the "
            "remainder of the title after the main title. Possible title component."
        ),
    )

    class Meta:
        ordering = ["main_title", "subtitle"]
        unique_together = ["main_title", "subtitle"]

    def __str__(self) -> str:
        if self.subtitle:
            return f"{self.main_title}: {self.subtitle}"

        return self.main_title

    @staticmethod
    def get_or_create(
        title: str, subtitle: str = "", increment: bool = True
    ) -> Optional["Title"]:
        """Gets or creates a new title object. If `increment` is True and if the `title`
        is Untitled or Translation, it will automatically add a counter to the
        `main_title`."""
        if not title:
            return None

        if subtitle is None:
            subtitle = ""

        if increment:
            title_lower = title.lower()
            if title_lower in ["untitled", "translation"]:
                subtitle = (
                    Title.objects.filter(main_title__iexact=title_lower).count() + 1
                )

        title, _ = Title.objects.get_or_create(main_title=title, subtitle=subtitle)

        return title


class Resource(TimeStampedModel):
    """Resource reflecting a conceptual essence of a cataloging resource."""

    _is_paratext = models.BooleanField(default=False, editable=False)

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

    subjects = ControlledTermsField(
        ["fast-forms", "fast-topic", "rt-agt", "wikidata"],
        blank=True,
        help_text="Subject term(s) describing a resource",
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

    edition_enumeration = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="Enumeration of the edition; usually transcribed.",
    )
    summary = models.TextField(
        blank=True,
        null=True,
        help_text=(
            "Description of the content of a resource, such as an abstract, "
            "summary, citation, etc."
        ),
    )

    held_by = models.ManyToManyField(
        Agent,
        blank=True,
        related_name="resources",
        help_text="Entity holding the item or from which it is available.",
    )
    electronic_locator = models.URLField(
        max_length=1280,
        blank=True,
        null=True,
        help_text="Electronic location from which the resource is available.",
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
        unique_together = ["title", "date", "_is_paratext"]

    def __str__(self) -> str:
        title = self.title

        if self.date:
            title = f"{title} ({str(self.date)})"

        if self.is_paratext():
            title = f"[paratext] {title}"

        return title

    def get_authors(self) -> str:
        return "; ".join(
            [c.agent.name for c in self.contributions.filter(roles__label="author")]
        )

    get_authors.short_description = "Authors"

    def get_classification_edition(self) -> str:
        return "; ".join([c.edition.label for c in self.classifications.all()])

    get_classification_edition.short_description = "Edition"  # type: ignore

    def get_language_names(self) -> str:
        return "; ".join([rl.language.label for rl in self.languages.all()])

    get_language_names.short_description = "Languages"  # type: ignore

    def get_place_names(self) -> str:
        return "; ".join([rp.place.address for rp in self.places.all()])

    get_place_names.short_description = "Places"  # type: ignore

    def is_original(self) -> bool:
        return "original" in self.get_classification_edition().lower()

    is_original.boolean = True  # type: ignore

    def is_paratext(self) -> bool:
        return (
            self.relationships.filter(relationship_type__label="paratext of").count()
            > 0
        )

    is_paratext.boolean = True  # type: ignore

    @staticmethod
    def from_gsx_entry(entry: Dict[str, Dict[str, str]]) -> Optional["Resource"]:
        """Gets or creates a new `Resource` from a Google Spreadsheet dictionary
        `entry`."""
        if not entry:
            return None

        main_title = get_gsx_entry_value(entry, "title")
        if not main_title:
            return None

        title = Title.get_or_create(main_title)
        date_display = get_gsx_entry_value(entry, "year")

        if date_display:
            resource, _ = Resource.objects.get_or_create(
                _is_paratext=False, title=title, date__date_display=date_display
            )

            date = Date.from_date_display(date_display)
            resource.date = date
        else:
            resource, _ = Resource.objects.get_or_create(
                _is_paratext=False, title=title
            )

        Contribution.from_gsx_entry(resource, entry, "authors", "author")

        Resource.languages_from_gsx_entry(resource, entry)

        Resource.subjects_from_gsx_entry(resource, entry)

        Classification.get_or_create(resource, get_gsx_entry_value(entry, "status"))

        value = get_gsx_entry_value(entry, "editionnumber")
        if value:
            resource.edition_enumeration = value

        value = get_gsx_entry_value(entry, "location")
        if value:
            for name in value.split("; "):
                place = get_geonames_place_from_gsx_place(name)
                if place:
                    ResourcePlace.objects.get_or_create(resource=resource, place=place)

        Contribution.from_gsx_entry(resource, entry, "organisation", "publisher")

        value = get_gsx_entry_value(entry, "notes")
        if value:
            resource.notes = value

        Resource.paratext_from_gsx_entry(entry, resource)

        libraries = get_gsx_entry_value(entry, "libraries")
        if libraries:
            for library in libraries.split("; "):
                library = library.strip()
                if library:
                    org, _ = Organisation.objects.get_or_create(name=library)
                    resource.held_by.add(org)

        url = get_gsx_entry_value(entry, "url")
        if url:
            resource.electronic_locator = url

        resource.save()

        return resource

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
                ResourceLanguage.objects.get_or_create(resource=resource, language=term)

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

    @staticmethod
    def paratext_from_gsx_entry(
        entry: Dict[str, Dict[str, str]], resource: "Resource"
    ) -> Optional["Resource"]:
        """Gets or creates a new paratext `Resource` from a Google Spreadsheet
        dictionary `entry`."""
        if not resource:
            return None

        citation = get_gsx_entry_value(entry, "citation")
        paratext_notes = get_gsx_entry_value(entry, "paratextnotes")

        if not citation and not paratext_notes:
            return None

        paratext, _ = Resource.objects.get_or_create(
            _is_paratext=True,
            title=resource.title,
            summary=citation,
            notes=paratext_notes,
        )

        ResourceRelationship.get_or_create(paratext, "paratext of", resource)

        return paratext

    @staticmethod
    def relationships_from_gsx_entry(
        entry: Dict[str, Dict[str, str]]
    ) -> Optional["Resource"]:
        if not entry:
            return None

        main_title = get_gsx_entry_value(entry, "title")
        if not main_title:
            return None

        title = Title.get_or_create(main_title)
        date_display = get_gsx_entry_value(entry, "year")

        try:
            if date_display:
                resource = Resource.objects.get(
                    _is_paratext=False, title=title, date__date_display=date_display
                )
            else:
                resource = Resource.objects.get(_is_paratext=False, title=title)
        except Resource.DoesNotExist:
            return None

        fields_mapping = {
            "part of": "partof",
            "translation of": "translationof",
            "other edition": "editionof",
        }

        for key in fields_mapping.keys():
            value = get_gsx_entry_value(entry, fields_mapping[key])
            if value:
                for main_title in value.split("; "):
                    main_title = main_title.strip()
                    if main_title:
                        related_to = Resource.objects.filter(
                            _is_paratext=False, title__main_title=main_title
                        ).first()
                        ResourceRelationship.get_or_create(resource, key, related_to)

        return resource


class Classification(TimeStampedModel, EditorialClassificationModel):
    """System of coding and organizing materials according to their subject."""

    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="classifications"
    )

    edition = ControlledTermField(
        ["rt-ppt", "rt-tt", "rt-pt"],
        on_delete=models.CASCADE,
        help_text=(
            "Edition of the classification scheme, such as full, abridged or a number, "
            "when a classification scheme designates editions."
        ),
    )

    def __str__(self) -> str:
        return self.edition.label

    @staticmethod
    def get_or_create(resource: Resource, term: str) -> Optional["Classification"]:
        if not resource or not term:
            return None

        term = term.replace("Translation: ", "")
        edition = search_term_or_none("rt-tt", term)

        if not edition:
            return None

        classification, _ = Classification.objects.get_or_create(
            resource=resource, edition=edition
        )

        return classification


class Contribution(TimeStampedModel, EditorialClassificationModel):
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
    published_as = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        help_text=(
            "Name as it appears in the published resource if different from the agent "
            "name. for pseudonyms, appelations, etc."
        ),
    )
    roles = ControlledTermsField(
        ["wikidata"],
        blank=True,
        help_text="Function provided by a contributor, e.g., author, illustrator, etc.",
    )

    def __str__(self) -> str:
        agent = self.agent
        if self.published_as:
            agent = f"{self.published_as} ({agent})"

        return f"{agent}"

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
                agent, _ = cls.objects.get_or_create(name=name)
                contributions.append(Contribution.get_or_create(resource, agent, role))
            except cls.DoesNotExist:
                pass

        return contributions

    @staticmethod
    def get_or_create(
        resource: Resource, agent: Agent, role: str, published_as: Optional[str] = None,
    ) -> Optional["Contribution"]:
        if not resource or not agent:
            return None

        contribution, _ = Contribution.objects.get_or_create(
            resource=resource, agent=agent, published_as=published_as
        )

        if role:
            term = search_term_or_none("wikidata", role)
            if term:
                contribution.roles.add(term)

        return contribution


class ResourceLanguage(TimeStampedModel, EditorialClassificationModel):
    """Language associated with a resource or its parts."""

    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="languages"
    )
    language = ControlledTermField(
        ["iso639-2"],
        on_delete=models.CASCADE,
        help_text="Language associated with a resource or its parts.",
    )

    class Meta:
        unique_together = ["resource", "language"]

    def __str__(self) -> str:
        return self.language.label


class ResourcePlace(TimeStampedModel, EditorialClassificationModel):
    """Geographic location or place entity associated with a resource or element
    of description, such as the place associated with the publication,
    printing, distribution, issue, release or production of a resource, place
    of an event."""

    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="places"
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        help_text=(
            "Geographic location or place entity associated with a resource or element "
            "of description, such as the place associated with the publication, "
            "printing, distribution, issue, release or production of a resource, place "
            "of an event."
        ),
    )

    class Meta:
        unique_together = ["resource", "place"]

    def __str__(self) -> str:
        return self.place.address


class ResourceRelationship(TimeStampedModel, EditorialClassificationModel):
    """Any relationship between resources."""

    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="relationships"
    )

    relationship_type = ControlledTermField(
        ["bf-crr"],
        on_delete=models.CASCADE,
        help_text="Any relationship between resources.",
    )
    related_to = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="related_to",
        help_text="Related resource.",
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
