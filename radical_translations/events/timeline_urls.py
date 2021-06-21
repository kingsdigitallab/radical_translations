from django.urls import path
from rest_framework.routers import DefaultRouter

from radical_translations.events.views import EventViewSet, event_grid

router = DefaultRouter()
router.register("api", basename="event-api", viewset=EventViewSet)

urlpatterns = [
    path("", event_grid, name="timeline"),
] + router.urls
