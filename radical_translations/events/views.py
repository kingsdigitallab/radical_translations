from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from radical_translations.events.models import Event


class EventDetailView(DetailView):
    model = Event


class EventListView(ListView):
    model = Event
