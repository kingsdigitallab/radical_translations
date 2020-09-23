from django.shortcuts import render
from django.views.generic.detail import DetailView
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from radical_translations.core.documents import ResourceDocument
from radical_translations.core.models import Resource
from radical_translations.core.serializers import ResourceDocumentSerializer


class ResourceDetailView(DetailView):
    model = Resource


def resource_list(request):
    return render(request, "core/resource_list.html")


class ResourceViewSet(DocumentViewSet):
    document = ResourceDocument
    serializer_class = ResourceDocumentSerializer

    filter_backends = [SearchFilterBackend]
    lookup_field = "id"
    ordering = ["title.main_title", "date_earliest", "date_latest"]
    page_size = 50
    search_fields = ["title.main_title", "languages.language.label"]
