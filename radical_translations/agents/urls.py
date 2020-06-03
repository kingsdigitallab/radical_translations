from django.urls import path

from radical_translations.agents.views import (
    AgentDetailView,
    OrganisationListView,
    PersonListView,
)

urlpatterns = [
    path("organisations/", OrganisationListView.as_view(), name="organisation-list"),
    path("persons/", PersonListView.as_view(), name="person-list"),
    path("<int:pk>/", AgentDetailView.as_view(), name="agent-detail"),
]
