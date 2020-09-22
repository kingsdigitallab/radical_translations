from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from radical_translations.core.documents import ResourceDocument


class ResourceDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ResourceDocument
