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
    HighlightBackend,
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
ES_FUZZINESS_OPTIONS = settings.ES_FUZZINESS_OPTIONS


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
        CompoundSearchFilterBackend,
        SearchFilterBackend,
        HighlightBackend,
        # the suggester backend needs to be the last backend
        SuggesterFilterBackend,
    ]

    lookup_field = "id"

    faceted_search_fields = {
        "classification_paratext": {
            "field": "classifications_paratext.edition.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "classification_printing_publishing": {
            "field": "classifications_printing_publishing.edition.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "classification_translation": {
            "field": "classifications_translation.edition.label.raw",
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
        "form_genre": {
            "field": "form_genre.label.raw",
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
        "classification_paratext": "classifications_paratext.edition.label.raw",
        "classification_printing_publishing": (
            "classifications_printing_publishing.edition.label.raw"
        ),
        "classification_translation": "classifications_translation.edition.label.raw",
        "contributor": "contributions.agent.name.raw",
        "contributor_role": "contributions.roles.label.raw",
        "date": "year_earliest",
        "form_genre": "form_genre.label.raw",
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

    highlight_fields = {
        "title.main_title": {
            "enabled": True,
            "options": {
                "number_of_fragments": 0,
                "pre_tags": ["<span class='highlight'>"],
                "post_tags": ["</span>"],
            },
        }
    }

    ordering_fields = {
        "title": "title.main_title.sort",
        "date": "year_earliest",
    }
    ordering = ["title", "date"]

    pagination_class = PageNumberPagination

    search_fields = {
        "title.main_title": ES_FUZZINESS_OPTIONS,
        "authors.person.name": ES_FUZZINESS_OPTIONS,
        "summary": None,
    }

    suggester_fields = {
        "suggest_field": {
            "field": "authors.person.name.suggest",
            "suggesters": [SUGGESTER_COMPLETION, SUGGESTER_PHRASE, SUGGESTER_TERM],
            "default_suggester": SUGGESTER_COMPLETION,
            "options": {"skip_duplicates": True, "size": 20},
        },
    }
