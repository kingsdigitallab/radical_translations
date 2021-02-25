from django.conf import settings
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
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

from radical_translations.agents.documents import PersonDocument
from radical_translations.agents.models import Agent, Organisation
from radical_translations.agents.serializers import PersonDocumentSerializer
from radical_translations.utils.search import PageNumberPagination

# from django_elasticsearch_dsl_drf.constants import (
# SUGGESTER_COMPLETION,
# SUGGESTER_PHRASE,
# SUGGESTER_TERM,
# )


ES_FACET_OPTIONS = settings.ES_FACET_OPTIONS
ES_FUZZINESS_OPTIONS = settings.ES_FUZZINESS_OPTIONS


class AgentDetailView(DetailView):
    model = Agent


class OrganisationListView(ListView):
    model = Organisation
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Organisations"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(roles__label="library")
        return queryset


def person_list(request):
    return render(request, "agents/person_list.html")


class PersonViewSet(DocumentViewSet):
    document = PersonDocument
    serializer_class = PersonDocumentSerializer

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
            "field": "place_birth.place.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "place_death": {
            "field": "place_death.place.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "noble": {
            "field": "noble",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "based_near": {
            "field": "based_near.place.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "main_place": {
            "field": "main_places.place.address.raw",
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
        "year": "year",
    }

    ordering_fields = {
        "name": "name.sort",
        "year": "year",
    }
    ordering = ["_score", "name.sort", "year"]

    pagination_class = PageNumberPagination

    search_fields = {
        "name": ES_FUZZINESS_OPTIONS,
    }

    # suggester_fields = {
    # "suggest_field": {
    # "field": "authors.person.name.suggest",
    # "suggesters": [SUGGESTER_COMPLETION, SUGGESTER_PHRASE, SUGGESTER_TERM],
    # "default_suggester": SUGGESTER_COMPLETION,
    # "options": {"skip_duplicates": True, "size": 20},
    # },
    # }
