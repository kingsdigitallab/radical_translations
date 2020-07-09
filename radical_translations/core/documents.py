from controlled_vocabulary.models import ControlledTerm
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from radical_translations.core.models import Resource, Title


@registry.register_document
class ResourceDocument(Document):
    title = fields.ObjectField(
        properties={"main_title": fields.TextField(), "subtitle": fields.TextField()}
    )
    subjects = fields.ObjectField(
        properties={"termid": fields.TextField(), "label": fields.TextField()}
    )

    class Index:
        name = "resources"

    class Django:
        model = Resource
        fields = ["id"]

        related_models = [ControlledTerm, Title]

    def get_queryset(self):
        return super().get_queryset().select_related("title")

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, ControlledTerm):
            return related_instance.resources.all()

        if isinstance(related_instance, Title):
            return related_instance.resources.all()
