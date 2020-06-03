from django.urls import path

from radical_translations.events.views import EventDetailView, EventListView

urlpatterns = [
    path("<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("", EventListView.as_view(), name="event-list"),
]
