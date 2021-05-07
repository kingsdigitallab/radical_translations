from django.urls import path
from rest_framework.routers import DefaultRouter

from radical_translations.events.views import (
    EventDetailView,
    EventViewSet,
    TimelineMockupPageView,
    event_grid,
    event_list,
)

router = DefaultRouter()
router.register("api", basename="event-api", viewset=EventViewSet)

urlpatterns = [
    path("<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("", event_list, name="event-list"),
    path("grid/", event_grid, name="event-grid"),
    path("timeline-mockup/", TimelineMockupPageView.as_view(), name="timeline-mockup"),
] + router.urls
