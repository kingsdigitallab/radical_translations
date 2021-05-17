from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from radical_translations.events.documents import EventDocument


class EventDocumentSerializer(DocumentSerializer):
    class Meta:
        document = EventDocument
