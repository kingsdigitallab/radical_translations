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
from radical_translations.core.serializers import (
    ResourceDocumentSerializer,
    SimpleResourceDocumentSerializer,
)
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
        "paratext_forms": {
            "field": "classifications_paratext.edition.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "printing_and_publishing_status": {
            "field": "classifications_printing_publishing.edition.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "translations_status": {
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
        "year": {
            "field": "year",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "language": {
            "field": "languages.label.raw",
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
        "meta": {"field": "meta", "enabled": True, "options": ES_FACET_OPTIONS},
    }

    filter_fields = {
        "paratext_forms": "classifications_paratext.edition.label.raw",
        "printing_and_publishing_status": (
            "classifications_printing_publishing.edition.label.raw"
        ),
        "translations_status": "classifications_translation.edition.label.raw",
        "contributor": "contributions.agent.name.raw",
        "contributor_role": "contributions.roles.label.raw",
        "year": "year",
        "form_genre": "form_genre.label.raw",
        "language": "languages.label.raw",
        "publication_place": "places.place.address.raw",
        "publication_country": "places.place.country.name.raw",
        "fictional_place_of_publication": "places.fictional_place.raw",
        "status": "relationships.relationship_type.label.raw",
        "subject": "subjects.label.raw",
        "event": "events.title.raw",
        "event_place": "events.place.address.raw",
        "meta": "meta",
    }

    highlight_fields = {
        "title": {
            "enabled": True,
            "options": {
                "number_of_fragments": 0,
                "pre_tags": ["<span class='highlight'>"],
                "post_tags": ["</span>"],
            },
        },
        "content": {
            "enabled": True,
            "options": {
                "fragment_size": 150,
                "number_of_fragments": 3,
                "pre_tags": ["<span class='highlight'>"],
                "post_tags": ["</span>"],
            },
        },
    }

    ordering_fields = {
        "title": "title.sort",
        "year": "year",
    }
    ordering = ["_score", "title.sort", "year"]

    pagination_class = PageNumberPagination

    title_search_options = ES_FUZZINESS_OPTIONS
    title_search_options["boost"] = 4
    author_search_options = ES_FUZZINESS_OPTIONS
    author_search_options["boost"] = 2

    search_fields = {
        "title": title_search_options,
        "authors.person.name": author_search_options,
        "content": ES_FUZZINESS_OPTIONS,
    }

    suggester_fields = {
        "suggest_field": {
            "field": "authors.person.name.suggest",
            "suggesters": [SUGGESTER_COMPLETION, SUGGESTER_PHRASE, SUGGESTER_TERM],
            "default_suggester": SUGGESTER_COMPLETION,
            "options": {"skip_duplicates": True, "size": 20},
        },
    }


class SimpleResourceViewSet(DocumentViewSet):
    document = ResourceDocument
    serializer_class = SimpleResourceDocumentSerializer

    filter_backends = [
        FilteringFilterBackend,
        FacetedSearchFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    lookup_field = "id"

    faceted_search_fields = {
        "country": {
            "field": "places.place.country.name.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
    }

    filter_fields = {
        "country": "places.place.country.name.raw",
        "year": "year",
    }

    ordering_fields = {
        "year": "year",
    }
    ordering = ["year"]

    pagination_class = PageNumberPagination

    search_fields = {
        "content": ES_FUZZINESS_OPTIONS,
    }
