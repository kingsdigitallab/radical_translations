from django.conf import settings
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django_elasticsearch_dsl_drf.constants import (
    SUGGESTER_COMPLETION,
    SUGGESTER_PHRASE,
    SUGGESTER_TERM,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from radical_translations.agents.documents import AgentDocument
from radical_translations.agents.models import Agent
from radical_translations.agents.serializers import AgentDocumentSerializer
from radical_translations.utils.search import PageNumberPagination

ES_FACET_OPTIONS = settings.ES_FACET_OPTIONS
ES_FUZZINESS_OPTIONS = settings.ES_FUZZINESS_OPTIONS


class AgentDetailView(DetailView):
    model = Agent


def agent_list(request):
    return render(request, "agents/agent_list.html")


class AgentViewSet(DocumentViewSet):
    document = AgentDocument
    serializer_class = AgentDocumentSerializer

    filter_backends = [
        FilteringFilterBackend,
        FacetedSearchFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        SearchFilterBackend,
        # the suggester backend needs to be the last backend
        SuggesterFilterBackend,
    ]

    lookup_field = "id"

    faceted_search_fields = {
        "meta": {"field": "meta", "enabled": True, "options": ES_FACET_OPTIONS},
        "year": {
            "field": "year",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "gender": {
            "field": "gender",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "place_birth": {
            "field": "place_birth.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "place_death": {
            "field": "place_death.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "noble": {
            "field": "noble",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "main_place": {
            "field": "based_near.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "other_places": {
            "field": "main_places.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "role": {
            "field": "roles.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "language": {
            "field": "languages.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
    }

    filter_fields = {
        "meta": "meta",
        "year": "year",
        "gender": "gender",
        "place_birth": "place_birth.address.raw",
        "place_death": "place_death.address.raw",
        "noble": "noble",
        "other_places": "main_places.address.raw",
        "main_place": "based_near.address.raw",
        "role": "roles.label.raw",
        "language": "languages.label.raw",
    }

    ordering_fields = {
        "name": "name_sort",
        "year": "year",
    }
    ordering = ["_score", "name_sort", "year"]

    pagination_class = PageNumberPagination

    search_fields = {
        "name": ES_FUZZINESS_OPTIONS,
    }

    suggester_fields = {
        "suggest_field": {
            "field": "name.suggest",
            "suggesters": [SUGGESTER_COMPLETION, SUGGESTER_PHRASE, SUGGESTER_TERM],
            "default_suggester": SUGGESTER_COMPLETION,
            "options": {"skip_duplicates": True, "size": 20},
        },
    }
