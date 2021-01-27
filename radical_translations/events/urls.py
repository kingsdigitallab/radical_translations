from django.urls import path
from rest_framework.routers import DefaultRouter

from radical_translations.events.views import EventDetailView, EventViewSet, event_list

router = DefaultRouter()
router.register("api", basename="event-api", viewset=EventViewSet)

urlpatterns = [
    path("<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("", event_list, name="event-list"),
] + router.urls
