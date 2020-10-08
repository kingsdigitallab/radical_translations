from django.conf import settings
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django_elasticsearch_dsl_drf.constants import (
    SUGGESTER_COMPLETION,
    SUGGESTER_PHRASE,
    SUGGESTER_TERM,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from radical_translations.core.documents import ResourceDocument
from radical_translations.core.models import Resource
from radical_translations.core.serializers import ResourceDocumentSerializer
from radical_translations.utils.search import PageNumberPagination

ES_FACET_OPTIONS = settings.ES_FACET_OPTIONS


class ResourceDetailView(DetailView):
    model = Resource


def resource_list(request):
    return render(request, "core/resource_list.html")


class ResourceViewSet(DocumentViewSet):
    document = ResourceDocument
    serializer_class = ResourceDocumentSerializer

    filter_backends = [
        FilteringFilterBackend,
        FacetedSearchFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        # the suggester backend needs to be the last backend
        SuggesterFilterBackend,
    ]

    lookup_field = "id"

    faceted_search_fields = {
        "classification": {
            "field": "classifications.edition.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "contributor": {
            "field": "contributions.agent.name.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "contributor_role": {
            "field": "contributions.roles.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "date": {
            "field": "year_earliest",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "language": {
            "field": "languages.language.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "publication_place": {
            "field": "places.place.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "publication_country": {
            "field": "places.place.country.name.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "fictional_place_of_publication": {
            "field": "places.fictional_place.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "status": {
            "field": "relationships.relationship_type.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "subject": {
            "field": "subjects.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "event": {
            "field": "events.title.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "event_place": {
            "field": "events.place.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "radical_date": {
            "field": "has_date_radical",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
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

    ordering_fields = {
        "title": "title.main_title.sort",
        "date": "year_earliest",
    }
    ordering = ["title", "date"]

    pagination_class = PageNumberPagination

    search_fields = ["title.main_title", "summary"]

    suggester_fields = {
        "suggest_field": {
            "field": "title.main_title.suggest",
            "suggesters": [SUGGESTER_COMPLETION, SUGGESTER_PHRASE, SUGGESTER_TERM],
            "default_suggester": SUGGESTER_COMPLETION,
            "options": {"skip_duplicates": True},
        },
    }
