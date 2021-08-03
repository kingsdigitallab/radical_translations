from django.urls import path
from rest_framework.routers import DefaultRouter

from radical_translations.core.views import (
    ResourceDetailView,
    ResourceViewSet,
    SimpleResourceViewSet,
    network,
    resource_list,
)

router = DefaultRouter()
router.register("api", basename="resource-api", viewset=ResourceViewSet)
router.register(
    "api-simple", basename="resource-api-simple", viewset=SimpleResourceViewSet
)

urlpatterns = [
    path("<int:pk>/", ResourceDetailView.as_view(), name="resource-detail"),
    path("", resource_list, name="resource-list"),
    path("network/", network, name="resource-network"),
] + router.urls
