import pytest

from radical_translations.agents.documents import OrganisationDocument, PersonDocument
from radical_translations.agents.models import Organisation, Person

pytestmark = pytest.mark.django_db


class TestPersonDocument:
    def test_get_queryset(self):
        qs = PersonDocument().get_queryset()
        assert qs.model == Person


class TestOrganisationDocument:
    def test_get_queryset(self):
        qs = OrganisationDocument().get_queryset()
        assert qs.model == Organisation
