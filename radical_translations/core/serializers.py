from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from radical_translations.core.documents import ResourceDocument


class ResourceDocumentSerializer(DocumentSerializer):
    highlight = serializers.SerializerMethodField()

    class Meta:
        document = ResourceDocument

    def get_highlight(self, obj):
        print(obj.meta)
        if hasattr(obj.meta, "highlight"):
            return obj.meta.highlight.__dict__["_d_"]

        return {}
