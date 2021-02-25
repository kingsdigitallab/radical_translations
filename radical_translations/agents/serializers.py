from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from radical_translations.agents.documents import PersonDocument


class PersonDocumentSerializer(DocumentSerializer):
    class Meta:
        document = PersonDocument
