from django.urls import path
from rest_framework.routers import DefaultRouter

from radical_translations.core.views import (
    ResourceDetailView,
    ResourceViewSet,
    network,
    resource_list,
)

router = DefaultRouter()
router.register("api", basename="resource-api", viewset=ResourceViewSet)

urlpatterns = [
    path("<int:pk>/", ResourceDetailView.as_view(), name="resource-detail"),
    path("", resource_list, name="resource-list"),
    path("network/", network, name="network"),
] + router.urls
