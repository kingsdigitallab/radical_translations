import pytest

from radical_translations.agents.documents import PersonDocument
from radical_translations.agents.models import Person

pytestmark = pytest.mark.django_db


class TestPersonDocument:
    def test_get_queryset(self):
        qs = PersonDocument().get_queryset()
        assert qs.model == Person
