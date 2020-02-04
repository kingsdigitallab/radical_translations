from controlled_vocabulary.models import ControlledTermField, ControlledTermsField
from django.db import models
from geonames_place.models import Place
from model_utils.models import TimeStampedModel
from polymorphic.models import PolymorphicModel
from radical_translations.agents.models import Agent
from radical_translations.utils.models import Date

# These models are based on the BIBFRAME 2.0 Model
# https://www.loc.gov/bibframe/docs/bibframe2-model.html


class Title(TimeStampedModel):
    """Title information relating to a resource: work title, preferred title, instance
    title, transcribed title, translated title, variant form of title, etc."""

    main_title = models.CharField(
        max_length=256, help_text="Title being addressed. Possible title component."
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

    def __str__(self) -> str:
        return self.title.main_title


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
        return self.edition


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

    def __str__(self):
        return f"{self.resource} -> {self.relationship_type} -> {self.related_to}"


class Work(Resource):
    """The highest level of abstraction, a Work, in the BIBFRAME context, reflects the
    conceptual essence of the cataloged resource: authors, languages, and what it is
    about (subjects). """

    pass


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


class Item(Resource):
    """An item is an actual copy (physical or electronic) of an Instance. It reflects
    information such as its location (physical or virtual), shelf mark, and barcode."""

    pass
