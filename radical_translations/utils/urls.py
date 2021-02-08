from django.urls import path

from radical_translations.utils.views import PlaceRetrieveView

urlpatterns = [
    path("api/places/<int:pk>/", PlaceRetrieveView.as_view(), name="api-place-detail"),
]
