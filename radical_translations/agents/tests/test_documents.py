import pytest

from radical_translations.agents.documents import AgentDocument
from radical_translations.agents.models import Agent

pytestmark = pytest.mark.django_db


class TestAgentDocument:
    def test_get_queryset(self):
        qs = AgentDocument().get_queryset()
        assert qs.model == Agent
