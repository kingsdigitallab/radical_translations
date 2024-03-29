from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, normalizer

from controlled_vocabulary.models import ControlledTerm
from radical_translations.core.models import (
    Classification,
    Contribution,
    Resource,
    ResourceLanguage,
    ResourcePlace,
    ResourceRelationship,
    Title,
)
from radical_translations.utils.documents import (
    get_agent_field,
    get_controlled_term_field,
    get_place_field,
    get_resource_field,
)
from radical_translations.utils.models import Date

text_folding_analyzer = analyzer(
    "folding", tokenizer="standard", filter=["lowercase", "asciifolding"]
)
lowercase_sort_normalizer = normalizer(
    "lowercase_sort", filter=["lowercase", "asciifolding"]
)

copy_to_content = {"copy_to": "content"}


@registry.register_document
class ResourceDocument(Document):
    meta = fields.KeywordField()
    content = fields.TextField(attr="title.main_title", store=True)

    is_private = fields.BooleanField()

    title = fields.TextField(
        analyzer=text_folding_analyzer,
        fields={
            "raw": fields.KeywordField(),
            "sort": fields.KeywordField(normalizer=lowercase_sort_normalizer),
            "suggest": fields.CompletionField(),
        },
        **copy_to_content,
    )
    form_genre = get_controlled_term_field(options=copy_to_content)
    subjects = get_controlled_term_field(options=copy_to_content)
    date_display = fields.TextField(**copy_to_content)
    year = fields.IntegerField(**copy_to_content)
    summary = fields.TextField(**copy_to_content)
    classifications_printing_publishing = fields.ObjectField(
        properties={"edition": get_controlled_term_field(options=copy_to_content)}
    )
    classifications_translation = fields.ObjectField(
        properties={"edition": get_controlled_term_field(options=copy_to_content)}
    )
    classifications_paratext = fields.ObjectField(
        properties={"edition": get_controlled_term_field(options=copy_to_content)}
    )
    classifications_paratext_functions = fields.ObjectField(
        properties={"edition": get_controlled_term_field(options=copy_to_content)}
    )
    contributions = fields.ObjectField(
        properties={
            "agent": get_agent_field(options=copy_to_content),
            "roles": get_controlled_term_field(),
        }
    )
    published_as = fields.KeywordField()
    languages = get_controlled_term_field(options=copy_to_content)
    places = fields.ObjectField(
        properties={
            "place": get_place_field(options=copy_to_content),
            "fictional_place": fields.TextField(fields={"raw": fields.KeywordField()}),
        }
    )
    relationships = fields.ObjectField(
        properties={
            "relationship_type": get_controlled_term_field(options=copy_to_content),
            "related_to": get_resource_field(options=copy_to_content),
        }
    )

    # events = get_event_field(options=copy_to_content)

    is_original = fields.BooleanField()
    is_translation = fields.BooleanField()

    has_date_radical = fields.KeywordField()

    authors = fields.ObjectField(
        attr="get_authors_source_text",
        properties={"person": get_agent_field(options=copy_to_content)},
    )

    translated_from = get_controlled_term_field(options=copy_to_content)

    class Index:
        name = "rt-resources"

    class Django:
        model = Resource
        fields = ["id"]

        related_models = [
            Classification,
            Contribution,
            ControlledTerm,
            Date,
            ResourceLanguage,
            ResourcePlace,
            ResourceRelationship,
            Title,
        ]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .exclude(relationships__relationship_type__label="paratext of")
            .select_related("title", "date")
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Date):
            return related_instance.resource

        if isinstance(related_instance, (ControlledTerm, Title)):
            return related_instance.resources.all()

        if isinstance(
            related_instance,
            (
                Classification,
                Contribution,
                ResourceLanguage,
                ResourcePlace,
                ResourceRelationship,
            ),
        ):
            return related_instance.resource

    def prepare_meta(self, instance):
        if instance.is_original():
            return "source texts"

        meta = []

        if instance.get_paratext():
            meta.append("paratexts")

        if instance.is_translation():
            meta.append("translations")

        return meta

    def prepare_title(self, instance):
        titles = [str(instance.title)]

        for relationship in instance.get_paratext():
            paratext = relationship.resource
            if str(paratext.title) != str(instance.title):
                titles.append(str(paratext.title))

        return titles

    def prepare_form_genre(self, instance):
        return self._get_subjects(instance, ["fast-forms", "rt-agt"])

    def _get_subjects(self, instance, prefix):
        subjects = [
            {"label": item.label}
            for item in instance.subjects.filter(vocabulary__prefix__in=prefix)
        ]

        for relationship in instance.get_paratext():
            subjects.extend(self._get_subjects(relationship.resource, prefix))

        if subjects:
            subjects.append({"label": "any"})

        return subjects

    def prepare_subjects(self, instance):
        return self._get_subjects(instance, ["fast-topic"])

    def prepare_date_display(self, instance):
        resource = self._get_resource(instance)
        if resource.date:
            return str(resource.date)

    def _get_resource(self, resource):
        if resource.is_paratext():
            return resource.paratext_of()

        return resource

    def prepare_year(self, instance):
        resource = self._get_resource(instance)
        if resource.date:
            date_earliest = resource.date.get_date_earliest()
            date_latest = resource.date.get_date_latest()

            if date_earliest and date_latest:
                return [
                    year for year in range(date_earliest.year, date_latest.year + 1)
                ]

            if date_earliest:
                return date_earliest.year

            if date_latest:
                return date_latest.year

    def prepare_summary(self, instance):
        summaries = []

        if instance.summary:
            summaries = [instance.summary]

        for relationship in instance.get_paratext():
            if relationship.resource.summary:
                summaries.append(relationship.resource.summary)

        return summaries

    def prepare_classifications_printing_publishing(self, instance):
        return self._get_classifications(instance, "rt-ppt")

    def _get_classifications(self, instance, prefix):
        classifications = [
            {
                "edition": {"label": item.edition.label},
            }
            for item in instance.classifications.filter(
                edition__vocabulary__prefix=prefix
            )
            if item.edition.label.lower() not in ["original", "source-text"]
        ]

        for relationship in instance.get_paratext():
            classifications.extend(
                self._get_classifications(relationship.resource, prefix)
            )

        if classifications:
            classifications.append({"edition": {"label": "any"}})

        return classifications

    def prepare_classifications_translation(self, instance):
        return self._get_classifications(instance, "rt-tt")

    def prepare_classifications_paratext(self, instance):
        return self._get_classifications(instance, "rt-pt")

    def prepare_classifications_paratext_functions(self, instance):
        return self._get_classifications(instance, "rt-ptf")

    def prepare_contributions(self, instance):
        contributions = [
            {
                "agent": {
                    "id": item.agent.id,
                    "name": "Anonymous"
                    if item.agent.name.startswith("Anon")
                    else item.agent.get_index_name(),
                },
                "roles": [
                    {
                        "label": f"{role.label} of translation paratext"
                        if item.resource.is_paratext()
                        else role.label
                        for role in item.roles.all()
                    }
                ],
            }
            for item in instance.get_contributions(include_paratext=True)
        ]

        if contributions:
            contributions.append(
                {"agent": {"name": "any"}, "roles": [{"label": "any"}]}
            )

        return contributions

    def prepare_published_as(self, instance):
        published_as = []

        for item in instance.get_contributions(include_paratext=True):
            if item.published_as:
                published_as.append(item.published_as)

        if published_as:
            published_as.append("any")

        return published_as

    def prepare_languages(self, instance):
        languages = [
            {"label": item.language.label} for item in instance.languages.all()
        ]

        for relationship in instance.get_paratext():
            languages.extend(self.prepare_languages(relationship.resource))

        if languages:
            languages.append({"label": "any"})

        return languages

    def prepare_places(self, instance):
        places = []

        for item in instance.places.all():
            address = ""
            place = {}

            if item.fictional_place:
                address = item.fictional_place
                place = {
                    "fictional_place": item.fictional_place,
                    "place": {"address": address},
                }

            if item.place:
                address = (
                    f"{address} ({item.place.address})"
                    if address
                    else item.place.address
                )
                place["place"] = {
                    "address": address,
                    "geo": item.place.geo,
                    "country": {"name": item.place.country.name},
                }

            places.append(place)

        if places:
            places.append({"place": {"address": "any", "country": {"name": "any"}}})

        return places

    def prepare_relationships(self, instance):
        relationships = [
            {
                "relationship_type": {"label": item.relationship_type.label},
                "related_to": {
                    "id": item.related_to.id,
                    "title": {"main_title": str(item.related_to.title)},
                },
            }
            for item in instance.relationships.all()
        ]

        if relationships:
            relationships.append({"relationship_type": {"label": "any"}})

        return relationships

    def prepare_events(self, instance):
        events = [
            {
                "id": item.id,
                "title": item.title,
                "place": {
                    "address": item.place.address,
                    "country": {"name": item.place.country.name},
                },
            }
            for item in instance.events.all()
        ]

        if events:
            events.append(
                {
                    "title": "any",
                    "place": {"address": "any", "country": {"name": "any"}},
                }
            )

        return events

    def prepare_has_date_radical(self, instance):
        if instance.has_date_radical():
            return "yes"

        return "no"

    def prepare_translated_from(self, instance):
        languages = []

        if instance.get_languages_source_text():
            languages = [
                {"label": language.label}
                for language in instance.get_languages_source_text()
            ]

        if languages:
            languages.append({"label": "any"})

        return languages
