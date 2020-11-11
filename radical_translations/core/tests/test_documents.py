import pytest

from radical_translations.core.documents import ResourceDocument
from radical_translations.core.models import Resource
from radical_translations.utils.models import Date

pytestmark = pytest.mark.django_db


@pytest.fixture
@pytest.mark.usefixtures("entry_search")
def resource_for_search(entry_search):
    # setup
    resource = Resource.from_gsx_entry(entry_search)

    yield resource

    # teardown
    if resource.id:
        for rr in resource.related_to.all():
            rr.resource.delete()

        resource.delete()


class TestResourceDocument:
    def test_get_queryset(self):
        qs = ResourceDocument().get_queryset()
        assert qs.model == Resource

    @pytest.mark.usefixtures("resource_for_search")
    def test_get_instances_from_related(self, resource_for_search):
        resource = resource_for_search

        date_display = "2025"
        search = ResourceDocument.search().query("match", date_display=date_display)
        assert len(search.execute()) == 0

        resource.date.date_display = date_display
        resource.date.save()

        search = ResourceDocument.search().query("match", date_display=date_display)
        assert len(search.execute()) == 1

        label = "pytest"
        search = ResourceDocument.search().query("term", subjects__label=label)
        assert len(search.execute()) == 0

        subject = resource.subjects.first()
        subject.label = label
        subject.save()

        search = ResourceDocument.search().query("term", subjects__label=label)
        assert len(search.execute()) == subject.resources.count()

        search = ResourceDocument.search().query(
            "match_phrase", title__main_title=resource.title.main_title
        )
        assert len(search.execute()) == resource.title.resources.count()

        title = resource.title
        title.main_title = "radical translations"
        title.save()

        search = ResourceDocument.search().query(
            "match_phrase", title__main_title=resource.title.main_title
        )
        assert len(search.execute()) == title.resources.count()

        label = "pytest"
        search = ResourceDocument.search().query(
            "term", classifications__edition__label=label
        )
        assert len(search.execute()) == 0

        edition = resource.classifications.first().edition
        edition.label = label
        edition.save()

        search = ResourceDocument.search().query(
            "term", classifications__edition__label=label
        )
        assert len(search.execute()) == edition.resources.count()

        contribution = resource.contributions.first()
        agent = contribution.agent

        search = ResourceDocument.search().query(
            "match", contributions__agent__name=agent.name
        )
        assert len(search.execute()) == agent.contributed_to.count()

        agent.name = "change agent display name"
        agent.save()

        contribution.save()

        search = ResourceDocument.search().query(
            "match", contributions__agent__name=agent.name
        )
        assert len(search.execute()) == agent.contributed_to.count()

        label = "flemish"
        search = ResourceDocument.search().query(
            "term", languages_language__label=label
        )
        assert len(search.execute()) == 0

        language = resource.languages.first().language
        language.label = label
        language.save()

        search = ResourceDocument.search().query(
            "term", languages_language__label=label
        )
        assert len(search.execute()) == language.resources.count()

        label = "nowhere"
        search = ResourceDocument.search().query("match", places__fictional_place=label)
        assert len(search.execute()) == 0

        rp = resource.places.first()
        rp.fictional_place = label
        rp.save()

        search = ResourceDocument.search().query("match", places__fictional_place=label)
        assert len(search.execute()) == 1

    @pytest.mark.usefixtures("resource")
    def test_prepare_date_display(self, resource):
        doc = ResourceDocument()

        assert doc.prepare_date_display(resource) is None

        resource.date = Date(date_display="1971")
        resource.date.save()
        assert doc.prepare_date_display(resource) is not None

    @pytest.mark.usefixtures("entry_original")
    def test__get_resource(self, entry_original):
        doc = ResourceDocument()

        resource = Resource.from_gsx_entry(entry_original)
        assert doc._get_resource(resource) == resource

        paratext = Resource.paratext_from_gsx_entry(entry_original, resource)
        assert doc._get_resource(paratext) == resource

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
