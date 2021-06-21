from django.urls import path
from django.views.generic.base import RedirectView

from radical_translations.events.views import EventDetailView

urlpatterns = [
    path("<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("", RedirectView.as_view(pattern_name="timeline")),
]
