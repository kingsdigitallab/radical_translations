from django.views.generic.detail import DetailView

from geonames_place.models import Place


class PlaceDetailView(DetailView):
    model = Place
