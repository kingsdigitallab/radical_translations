from django.urls import path

from radical_translations.utils.views import PlaceDetailView

urlpatterns = [
    path("place/<int:pk>/", PlaceDetailView.as_view(), name="place-detail"),
]
