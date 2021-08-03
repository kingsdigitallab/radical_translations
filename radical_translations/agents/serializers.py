from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from radical_translations.agents.documents import AgentDocument


class AgentDocumentSerializer(DocumentSerializer):
    class Meta:
        document = AgentDocument
