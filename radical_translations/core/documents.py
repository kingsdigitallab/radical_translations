from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

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


@registry.register_document
class ResourceDocument(Document):
    title = fields.ObjectField(
        properties={"main_title": fields.TextField(), "subtitle": fields.TextField()}
    )
    subjects = get_controlled_term_field()
    date_earliest = fields.DateField()
    date_latest = fields.DateField()
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
        properties={"place": get_place_field(), "fictional_place": fields.TextField()}
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
        if isinstance(related_instance, (ControlledTerm, Date, Title)):
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

    def prepare_date_earliest(self, instance):
        resource = self._get_resource(instance)
        if resource.date and resource.date.date_earliest:
            return resource.date.get_date_earliest()

    def _get_resource(self, resource):
        if resource.is_paratext():
            return resource.paratext_of()

        return resource

    def prepare_date_latest(self, instance):
        resource = self._get_resource(instance)
        if resource.date and resource.date.date_latest:
            return resource.date.get_date_latest()

    def prepare_is_original(self, instance):
        return instance.is_original()

    def prepare_is_paratext(self, instance):
        return instance.is_paratext()
