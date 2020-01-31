from controlled_vocabulary.models import ControlledTermField, ControlledTermsField
from django.db import models
from model_utils.models import TimeStampedModel
from polymorphic.models import PolymorphicModel

from radical_translations.agents.models import Agent
from radical_translations.utils.models import Date

# These models are based on the BIBFRAME 2.0 Model
# https://www.loc.gov/bibframe/docs/bibframe2-model.html


class Source(TimeStampedModel):
    """Resource from which value or label came or was derived, such as the formal
    source/scheme from which a classification number is taken or derived, list from
    which an agent name is taken or derived, source within which an identifier is
    unique. """

    source = models.CharField(
        max_length=32,
        help_text="Resource from which value or label came or was derived",
    )

    def __str__(self) -> str:
        return self.source


class SourcedModel(models.Model):
    source = models.ManyToManyField(Source, blank=True)

    class Meta:
        abstract = True


class Classification(SourcedModel, TimeStampedModel):
    """System of coding and organizing materials according to their subject."""

    edition = models.CharField(
        max_length=64,
        help_text=(
            "Edition of the classification scheme, such as full, abridged or a number, "
            "when a classification scheme designates editions."
        ),
    )

    def __str__(self) -> str:
        return self.edition


class Note(TimeStampedModel):
    """Information, usually in textual form, on attributes of a resource or some aspect
    of a resource."""

    note = models.TextField()

    def __str__(self) -> str:
        return self.note


class NotesModel(models.Model):
    notes = models.ManyToManyField(
        Note,
        blank=True,
        help_text=(
            "Information, usually in textual form, on attributes of a resource or some "
            "aspect of a resource."
        ),
    )

    class Meta:
        abstract = True


class Role(TimeStampedModel):
    """Function played or provided by a contributor, e.g., author, illustrator, etc."""

    role = models.CharField(max_length=256, unique=True)

    def __str__(self) -> str:
        return self.role


class Contribution(NotesModel, TimeStampedModel):
    """Agent and role with respect to the resource being described."""

    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        help_text=(
            "Entity associated with a resource or element of description, such as the "
            "name of the entity responsible for the content or of the publication, "
            "printing, distribution, issue, release or production of a resource."
        ),
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        help_text="Function provided by a contributor, e.g., author, illustrator, etc.",
    )

    def __str__(self) -> str:
        return f"{self.role}: {self.agent}"


class ContributionsModel(models.Model):
    contributions = models.ManyToManyField(
        Contribution,
        blank=True,
        help_text="Agent and role with respect to the resource being described.",
    )

    class Meta:
        abstract = True


class Title(NotesModel, TimeStampedModel):
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


class Resource(PolymorphicModel, NotesModel, TimeStampedModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        help_text=(
            "Title information relating to a resource: work title, preferred title, "
            "instance title, transcribed title, translated title, variant form of "
            "title, etc."
        ),
    )

    classifications = models.ManyToManyField(
        Classification,
        blank=True,
        help_text=(
            "System of coding and organizing materials according to their subject."
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

    def __str__(self) -> str:
        return self.title.main_title


class ResourceRelationship(TimeStampedModel):
    """Any relationship between Work, Instance, and Item resources."""

    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="relationships"
    )
    relationship_type = ControlledTermField(["bf-crr"], on_delete=models.CASCADE)
    related_to = models.ForeignKey(Resource, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.resource} -> {self.relationship_type} -> {self.related_to}"


class Work(Resource, ContributionsModel):
    """The highest level of abstraction, a Work, in the BIBFRAME context, reflects the
    conceptual essence of the cataloged resource: authors, languages, and what it is
    about (subjects). """

    origin_date = models.OneToOneField(
        Date,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="Date or date range associated with the creation of a Work.",
    )


class Instance(Resource, ContributionsModel):
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
