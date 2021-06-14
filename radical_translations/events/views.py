from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from radical_translations.events.documents import EventDocument
from radical_translations.events.models import Event
from radical_translations.events.serializers import EventDocumentSerializer
from radical_translations.utils.search import PageNumberPagination

ES_FACET_OPTIONS = settings.ES_FACET_OPTIONS


class EventDetailView(DetailView):
    model = Event


def event_grid(request):
    return render(request, "events/event_grid.html")


class EventViewSet(DocumentViewSet):
    document = EventDocument
    serializer_class = EventDocumentSerializer

    filter_backends = [
        FilteringFilterBackend,
        FacetedSearchFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        SearchFilterBackend,
    ]

    lookup_field = "id"

    faceted_search_fields = {
        "year": {
            "field": "year",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "country": {
            "field": "country",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "type_of_event": {
            "field": "classification",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
    }

    filter_fields = {
        "year": "year",
        "country": "country",
        "type_of_event": "classification",
    }

    ordering_fields = {
        "country": "country",
        "year": "year",
    }
    ordering = ["country", "date_earliest"]

    pagination_class = PageNumberPagination


class TimelineMockupPageView(TemplateView):
    template_name = "events/timeline_mockup.html"
