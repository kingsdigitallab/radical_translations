from django.urls import path
from rest_framework.routers import DefaultRouter

from radical_translations.agents.views import (
    AgentDetailView,
    OrganisationListView,
    PersonViewSet,
    person_list,
)

router = DefaultRouter()
router.register("persons/api", basename="person-api", viewset=PersonViewSet)


urlpatterns = [
    path("organisations/", OrganisationListView.as_view(), name="organisation-list"),
    path("persons/", person_list, name="person-list"),
    path("<int:pk>/", AgentDetailView.as_view(), name="agent-detail"),
] + router.urls
