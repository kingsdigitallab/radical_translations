import pytest

from controlled_vocabulary.utils import search_term_or_none
from radical_translations.core.documents import ResourceDocument
from radical_translations.core.models import Classification, Resource, ResourceLanguage
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
            "match_phrase", title=resource.title.main_title
        )
        assert len(search.execute()) == resource.title.resources.count()

        title = resource.title
        title.main_title = "radical translations"
        title.save()

        search = ResourceDocument.search().query(
            "match_phrase", title=resource.title.main_title
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

    @pytest.mark.usefixtures("entry_original")
    def test_prepare_title(self, entry_original):
        doc = ResourceDocument()

        resource = Resource.from_gsx_entry(entry_original)
        paratext = Resource.paratext_from_gsx_entry(entry_original, resource)

        assert len(doc.prepare_title(resource)) == 1

        paratext.title.main_title = "a different title"
        paratext.title.save()
        paratext.save()

        assert len(doc.prepare_title(resource)) == 2

    @pytest.mark.usefixtures("entry_original")
    def test_prepare_form_genre(self, entry_original):
        doc = ResourceDocument()

        resource = Resource.from_gsx_entry(entry_original)
        paratext = Resource.paratext_from_gsx_entry(entry_original, resource)

        assert len(doc.prepare_form_genre(resource)) == 0

        resource.subjects.add(search_term_or_none("fast-forms", "History"))
        assert len(doc.prepare_form_genre(resource)) == 1

        paratext.subjects.add(search_term_or_none("fast-forms", "Periodicals"))
        assert len(doc.prepare_form_genre(resource)) == 2

    @pytest.mark.usefixtures("entry_original")
    def test__get_subjects(self, entry_original):
        doc = ResourceDocument()

        resource = Resource.from_gsx_entry(entry_original)

        assert len(doc._get_subjects(resource, "fast-forms")) == 0
        assert len(doc._get_subjects(resource, "fast-topic")) == 1

    @pytest.mark.usefixtures("entry_original")
    def test_prepare_subjects(self, entry_original):
        doc = ResourceDocument()

        resource = Resource.from_gsx_entry(entry_original)
        paratext = Resource.paratext_from_gsx_entry(entry_original, resource)

        assert len(doc.prepare_subjects(resource)) == 1

        paratext.subjects.add(search_term_or_none("fast-topic", "Operas"))
        assert len(doc.prepare_subjects(resource)) == 2

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

    @pytest.mark.usefixtures("entry_original")
    def test_prepare_classifications_printing_publishing(self, entry_original):
        doc = ResourceDocument()

        resource = Resource.from_gsx_entry(entry_original)
        paratext = Resource.paratext_from_gsx_entry(entry_original, resource)

        assert len(doc.prepare_classifications_printing_publishing(resource)) == 0

        resource.classifications.add(
            Classification(edition=search_term_or_none("rt-ppt", "Forgeries")),
            bulk=False,
        )
        assert len(doc.prepare_classifications_printing_publishing(resource)) == 1

        paratext.classifications.add(
            Classification(edition=search_term_or_none("rt-ppt", "Piracies")),
            bulk=False,
        )
        assert len(doc.prepare_classifications_printing_publishing(resource)) == 2

    @pytest.mark.usefixtures("entry_original")
    def test__get_classifications(self, entry_original):
        doc = ResourceDocument()

        resource = Resource.from_gsx_entry(entry_original)

        assert len(doc._get_classifications(resource, "rt-ppt")) == 0
        assert len(doc._get_classifications(resource, "rt-tt")) == 1
        assert len(doc._get_classifications(resource, "rt-pt")) == 0

    @pytest.mark.usefixtures("entry_original")
    def test_prepare_classifications_translation(self, entry_original):
        doc = ResourceDocument()

        resource = Resource.from_gsx_entry(entry_original)
        paratext = Resource.paratext_from_gsx_entry(entry_original, resource)

        assert len(doc.prepare_classifications_translation(resource)) == 1

        resource.classifications.add(
            Classification(edition=search_term_or_none("rt-tt", "Integral")),
            bulk=False,
        )
        assert len(doc.prepare_classifications_translation(resource)) == 2

        paratext.classifications.add(
            Classification(edition=search_term_or_none("rt-tt", "Partial")),
            bulk=False,
        )
        assert len(doc.prepare_classifications_translation(resource)) == 3

    @pytest.mark.usefixtures("entry_original")
    def test_prepare_classifications_paratext(self, entry_original):
        doc = ResourceDocument()

        resource = Resource.from_gsx_entry(entry_original)
        paratext = Resource.paratext_from_gsx_entry(entry_original, resource)

        assert len(doc.prepare_classifications_paratext(resource)) == 0

        paratext.classifications.add(
            Classification(edition=search_term_or_none("rt-pt", "Preface")),
            bulk=False,
        )
        assert len(doc.prepare_classifications_paratext(resource)) == 1

    @pytest.mark.usefixtures("entry_original")
    def test_prepare_languages(self, entry_original):
        doc = ResourceDocument()

        resource = Resource.from_gsx_entry(entry_original)
        paratext = Resource.paratext_from_gsx_entry(entry_original, resource)

        assert len(doc.prepare_languages(resource)) == 1

        paratext.languages.add(
            ResourceLanguage(language=search_term_or_none("iso639-2", "english")),
            bulk=False,
        )
        assert len(doc.prepare_languages(resource)) == 2
