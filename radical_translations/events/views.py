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


def event_list(request):
    return render(request, "events/event_list.html")


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
            "field": "place.country.name.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "classification": {
            "field": "classification.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
    }

    filter_fields = {
        "year": "year",
        "country": "place.country.name.raw",
        "classification": "classification.label.raw",
    }

    ordering_fields = {
        "date_earliest": "date_earliest",
        "date_latest": "date_latest",
        "year": "year",
    }
    ordering = ["_score", "date_earliest", "date_latest"]

    pagination_class = PageNumberPagination


class TimelineMockupPageView(TemplateView):
    template_name = "events/timeline_mockup.html"
