from django.urls import path
from rest_framework.routers import DefaultRouter

from radical_translations.agents.views import AgentDetailView, AgentViewSet, agent_list

router = DefaultRouter()
router.register("api", basename="agent-api", viewset=AgentViewSet)


urlpatterns = [
    path("", agent_list, name="agent-list"),
    path("<int:pk>/", AgentDetailView.as_view(), name="agent-detail"),
] + router.urls
