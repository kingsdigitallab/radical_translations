from django.shortcuts import render
from django.views.generic.detail import DetailView
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from elasticsearch_dsl import HistogramFacet, TermsFacet

from radical_translations.core.documents import ResourceDocument
from radical_translations.core.models import Resource
from radical_translations.core.serializers import ResourceDocumentSerializer
from radical_translations.utils.search import PageNumberPagination


class ResourceDetailView(DetailView):
    model = Resource


def resource_list(request):
    return render(request, "core/resource_list.html")


class ResourceViewSet(DocumentViewSet):
    document = ResourceDocument
    serializer_class = ResourceDocumentSerializer

    filter_backends = [
        DefaultOrderingFilterBackend,
        FacetedSearchFilterBackend,
        FilteringFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
    ]

    lookup_field = "id"

    faceted_search_fields = {
        "date": {
            "field": "year_earliest",
            "facet": HistogramFacet,
            "enabled": True,
            "options": {"interval": 50},
        },
        "language": {
            "field": "languages.language.label.raw",
            "facet": TermsFacet,
            "enabled": True,
        },
        "paratext": {
            "field": "is_paratext",
            "facet": TermsFacet,
            "enabled": True,
        },
        "subject": {
            "field": "subjects.label.raw",
            "facet": TermsFacet,
            "enabled": True,
        },
    }

    filter_fields = {
        "date": "year_earliest",
        "language": "languages.language.label.raw",
        "paratext": "is_paratext",
        "subject": "subjects.label.raw",
    }

    ordering_fields = {"title": "title.main_title.raw", "date": "year_earliest"}
    ordering = ["title", "date"]

    pagination_class = PageNumberPagination

    search_fields = ["title.main_title", "languages.language.label"]
