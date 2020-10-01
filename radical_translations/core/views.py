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

    facet_options = {"order": {"_key": "asc"}, "size": 100}

    faceted_search_fields = {
        "classification": {
            "field": "classifications.edition.label.raw",
            "enabled": True,
            "options": facet_options,
        },
        "contributor": {
            "field": "contributions.agent.name.raw",
            "enabled": True,
            "options": facet_options,
        },
        "contributor_role": {
            "field": "contributions.roles.label.raw",
            "enabled": True,
            "options": facet_options,
        },
        "date": {"field": "year_earliest", "enabled": True, "options": facet_options},
        "language": {
            "field": "languages.language.label.raw",
            "enabled": True,
            "options": facet_options,
        },
        "publication_place": {
            "field": "places.place.address.raw",
            "enabled": True,
            "options": facet_options,
        },
        "publication_country": {
            "field": "places.place.country.name.raw",
            "enabled": True,
            "options": facet_options,
        },
        "fictional_place_of_publication": {
            "field": "places.fictional_place.raw",
            "enabled": True,
            "options": facet_options,
        },
        "status": {
            "field": "relationships.relationship_type.label.raw",
            "enabled": True,
            "options": facet_options,
        },
        "subject": {
            "field": "subjects.label.raw",
            "enabled": True,
            "options": facet_options,
        },
        "event": {
            "field": "events.title.raw",
            "enabled": True,
            "options": facet_options,
        },
        "event_place": {
            "field": "events.place.address.raw",
            "enabled": True,
            "options": facet_options,
        },
        "radical_date": {
            "field": "has_date_radical",
            "enabled": True,
            "options": facet_options,
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
