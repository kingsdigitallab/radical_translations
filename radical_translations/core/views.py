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
from elasticsearch_dsl import TermsFacet

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
        "classification": {
            "field": "classifications.edition.label.raw",
            "facet": TermsFacet,
            "enabled": True,
        },
        "contributor": {
            "field": "contributions.agent.name.raw",
            "facet": TermsFacet,
            "enabled": True,
        },
        "contributor_role": {
            "field": "contributions.roles.label.raw",
            "facet": TermsFacet,
            "enabled": True,
        },
        "date": {
            "field": "year_earliest",
            "facet": TermsFacet,
            "enabled": True,
        },
        "language": {
            "field": "languages.language.label.raw",
            "facet": TermsFacet,
            "enabled": True,
        },
        "publication_place": {
            "field": "places.place.address.raw",
            "facet": TermsFacet,
            "enabled": True,
        },
        "publication_country": {
            "field": "places.place.country.name.raw",
            "facet": TermsFacet,
            "enabled": True,
        },
        "fictional_place_of_publication": {
            "field": "places.fictional_place.raw",
            "facet": TermsFacet,
            "enabled": True,
        },
        "status": {
            "field": "relationships.relationship_type.label.raw",
            "facet": TermsFacet,
            "enabled": True,
        },
        "subject": {
            "field": "subjects.label.raw",
            "facet": TermsFacet,
            "enabled": True,
        },
        "event": {
            "field": "events.title.raw",
            "facet": TermsFacet,
            "enabled": True,
        },
        "event_place": {
            "field": "events.place.address.raw",
            "facet": TermsFacet,
            "enabled": True,
        },
        "radical_date": {
            "field": "has_date_radical",
            "facet": TermsFacet,
            "enabled": True,
        },
    }

    filter_fields = {
        "classification": "classifications.edition.label.raw",
        "contributor": "contributions.agent.name.raw",
        "contributor_role": "contributions.roles.label.raw",
        "date": "year_earliest",
        "language": "languages.language.label.raw",
        "publication_place": "places.place.address.raw",
        "publication_country": "places.place.country.raw",
        "fictional_place_of_publication": "places.fictional_place.raw",
        "status": "relationships.relationship_type.label.raw",
        "subject": "subjects.label.raw",
        "event": "events.title.raw",
        "event_place": "events.place.address.raw",
        "radical_date": "has_date_radical",
    }

    ordering_fields = {"title": "title.main_title.raw", "date": "year_earliest"}
    ordering = ["title", "date"]

    pagination_class = PageNumberPagination

    search_fields = ["title.main_title"]
