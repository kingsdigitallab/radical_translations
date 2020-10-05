import pytest

from radical_translations.core.documents import ResourceDocument
from radical_translations.core.models import Resource
from radical_translations.utils.models import Date

pytestmark = pytest.mark.django_db


class TestResourceDocument:
    def test_get_queryset(self):
        qs = ResourceDocument().get_queryset()
        assert qs.model == Resource

    @pytest.mark.usefixtures("resource")
    def test_prepare_year_earliest(self, resource):
        doc = ResourceDocument()

        prepared_data = doc.prepare_year_earliest(resource)
        assert prepared_data is None

        resource.date = Date(date_display="1971")
        resource.date.save()

        prepared_data = doc.prepare_year_earliest(resource)
        assert prepared_data is not None
        assert prepared_data == 1971

    @pytest.mark.usefixtures("entry_original")
    def test__get_resource(self, entry_original):
        doc = ResourceDocument()

        resource = Resource.from_gsx_entry(entry_original)
        assert doc._get_resource(resource) == resource

        paratext = Resource.paratext_from_gsx_entry(entry_original, resource)
        assert doc._get_resource(paratext) == resource

    @pytest.mark.usefixtures("resource")
    def test_prepare_year_latest(self, resource):
        doc = ResourceDocument()

        prepared_data = doc.prepare_year_latest(resource)
        assert prepared_data is None

        resource.date = Date(date_display="1971")
        resource.date.save()

        prepared_data = doc.prepare_year_latest(resource)
        assert prepared_data is not None
        assert prepared_data == 1971
