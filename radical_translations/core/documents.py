from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, normalizer

from controlled_vocabulary.models import ControlledTerm
from radical_translations.core.models import (
    Classification,
    Contribution,
    Resource,
    ResourceLanguage,
    ResourcePlace,
    ResourceRelationship,
    Title,
)
from radical_translations.utils.documents import (
    get_agent_field,
    get_controlled_term_field,
    get_event_field,
    get_place_field,
    get_resource_field,
)
from radical_translations.utils.models import Date

text_folding_analyzer = analyzer(
    "folding", tokenizer="standard", filter=["lowercase", "asciifolding"]
)
lowercase_sort_normalizer = normalizer(
    "lowercase_sort", filter=["lowercase", "asciifolding"]
)

kwargs = {"copy_to": "content"}


@registry.register_document
class ResourceDocument(Document):
    content = fields.TextField(attr="title.main_title")

    title = fields.ObjectField(
        properties={
            "main_title": fields.TextField(
                analyzer=text_folding_analyzer,
                fields={
                    "raw": fields.KeywordField(),
                    "sort": fields.KeywordField(normalizer=lowercase_sort_normalizer),
                    "suggest": fields.CompletionField(),
                },
                **kwargs
            ),
            "subtitle": fields.TextField(),
        },
    )
    form_genre = get_controlled_term_field()
    subjects = get_controlled_term_field()
    date_display = fields.TextField()
    year_earliest = fields.IntegerField()
    year_latest = fields.IntegerField()
    summary = fields.TextField(**kwargs)
    classifications = fields.ObjectField(
        properties={
            "classification": get_controlled_term_field(),
            "edition": get_controlled_term_field(),
        }
    )
    contributions = fields.ObjectField(
        properties={
            "agent": get_agent_field(),
            "published_as": fields.TextField(),
            "roles": get_controlled_term_field(),
        }
    )
    languages = fields.ObjectField(properties={"language": get_controlled_term_field()})
    places = fields.ObjectField(
        properties={
            "place": get_place_field(),
            "fictional_place": fields.TextField(fields={"raw": fields.KeywordField()}),
        }
    )
    relationships = fields.ObjectField(
        properties={
            "relationship_type": get_controlled_term_field(),
            "related_to": get_resource_field(),
        }
    )

    events = get_event_field()

    is_original = fields.BooleanField()
    is_paratext = fields.BooleanField()
    is_translation = fields.BooleanField()

    has_date_radical = fields.BooleanField()

    authors = fields.ObjectField(
        attr="get_authors_source_text", properties={"person": get_agent_field()}
    )

    class Index:
        name = "rt-resources"

    class Django:
        model = Resource
        fields = ["id"]

        related_models = [
            Classification,
            Contribution,
            ControlledTerm,
            Date,
            ResourceLanguage,
            ResourcePlace,
            ResourceRelationship,
            Title,
        ]

    def get_queryset(self):
        return super().get_queryset().select_related("title", "date")

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Date):
            return related_instance.resource

        if isinstance(related_instance, (ControlledTerm, Title)):
            return related_instance.resources.all()

        if isinstance(
            related_instance,
            (
                Classification,
                Contribution,
                ResourceLanguage,
                ResourcePlace,
                ResourceRelationship,
            ),
        ):
            return related_instance.resource

    def prepare_form_genre(self, instance):
        return [
            {"label": item.label}
            for item in instance.subjects.filter(vocabulary__prefix="fast-forms")
        ]

    def prepare_subjects(self, instance):
        return [
            {"label": item.label}
            for item in instance.subjects.filter(vocabulary__prefix="fast-topics")
        ]

    def prepare_date_display(self, instance):
        resource = self._get_resource(instance)
        if resource.date:
            return str(resource.date)

    def _get_resource(self, resource):
        if resource.is_paratext():
            return resource.paratext_of()

        return resource

    def prepare_year_earliest(self, instance):
        resource = self._get_resource(instance)
        if resource.date and resource.date.date_earliest:
            date_earliest = resource.date.get_date_earliest()
            if date_earliest is not None:
                return date_earliest.year

    def prepare_year_latest(self, instance):
        resource = self._get_resource(instance)
        if resource.date and resource.date.date_latest:
            date_latest = resource.date.get_date_latest()
            if date_latest is not None:
                return date_latest.year
