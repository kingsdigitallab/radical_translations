from django.urls import path
from rest_framework.routers import DefaultRouter

from radical_translations.events.views import (
    EventDetailView,
    EventViewSet,
    event_list,
    TimelineMockupPageView,
)

router = DefaultRouter()
router.register("api", basename="event-api", viewset=EventViewSet)

urlpatterns = [
    path("<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("", event_list, name="event-list"),
    path("timeline-mockup/", TimelineMockupPageView.as_view(), name="timeline-mockup"),
] + router.urls
