from django.urls import path
from rest_framework.routers import DefaultRouter

from radical_translations.events.views import EventDetailView, EventViewSet, event_grid

router = DefaultRouter()
router.register("api", basename="event-api", viewset=EventViewSet)

urlpatterns = [
    path("<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("", event_grid, name="event-grid"),
] + router.urls
