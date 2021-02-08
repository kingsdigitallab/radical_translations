from rest_framework.generics import RetrieveAPIView

from geonames_place.models import Place
from geonames_place.serializers import PlaceSerializer


class PlaceRetrieveView(RetrieveAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
