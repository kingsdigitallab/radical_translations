from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from controlled_vocabulary.models import ControlledTerm
from geonames_place.models import Place
from radical_translations.core.models import Resource
from radical_translations.events.models import Event
from radical_translations.utils.documents import get_place_field, get_resource_field
from radical_translations.utils.models import Date


@registry.register_document
class EventDocument(Document):
    title = fields.TextField()

    date_earliest = fields.DateField()
    date_latest = fields.DateField()

    place = get_place_field()

    related_to = get_resource_field()

    class Index:
        name = "rt-events"

    class Django:
        model = Event
        fields = ["id"]

    def get_queryset(self):
        return super().get_queryset().select_related("date")

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Date):
            return related_instance.event

        if isinstance(related_instance, (ControlledTerm, Place, Resource)):
            return related_instance.events.all()

    def prepare_date_earliest(self, instance):
        if instance.date and instance.date.date_earliest:
            return instance.date.get_date_earliest()

    def prepare_date_latest(self, instance):
        if instance.date and instance.date.date_latest:
            return instance.date.get_date_latest()
