from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from controlled_vocabulary.models import ControlledTerm
from geonames_place.models import Place
from radical_translations.agents.models import Organisation, Person
from radical_translations.core.models import Contribution
from radical_translations.utils.documents import (
    get_agent_field,
    get_controlled_term_field,
    get_place_field,
    get_resource_field,
)
from radical_translations.utils.models import Date


class AgentDocument(Document):
    name = fields.TextField(fields={"sort": fields.KeywordField()})
    based_near = get_place_field()
    roles = get_controlled_term_field()
    sources = get_resource_field()

    contributed_to = fields.ObjectField(
        properties={
            "resource": get_resource_field(),
            "roles": get_controlled_term_field(),
        }
    )

    class Django:
        fields = ["id", "notes"]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Contribution):
            return related_instance.agent


@registry.register_document
class PersonDocument(AgentDocument):
    gender = fields.KeywordField()
    noble = fields.BooleanField()

    main_places = get_place_field()
    year = fields.IntegerField()
    date_display = fields.TextField()
    place_birth = get_place_field()
    place_death = get_place_field()

    languages = get_controlled_term_field()

    knows = get_agent_field()
    member_of = get_agent_field()

    class Index:
        name = "rt-persons"

    class Django:
        model = Person
        fields = ["id", "notes"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "date_birth",
                "place_birth",
                "date_death",
                "place_death",
            )
        )

    def get_instances_from_related(self, related_instance):
        super().get_instances_from_related(related_instance)

        if isinstance(related_instance, Date):
            if related_instance.person_birth:
                return related_instance.person_birth

            return related_instance.person_death

        if isinstance(related_instance, (ControlledTerm, Place)):
            return related_instance.persons.all()

    def prepare_year(self, instance):
        date_birth = instance.date_birth
        year_birth = None

        if date_birth and date_birth.get_date_earliest():
            year_birth = date_birth.get_date_earliest().year

        date_death = instance.date_death
        year_death = None

        if date_death and date_death.get_date_latest():
            year_death = date_death.get_date_latest().year

        if year_birth and year_death:
            return [year for year in range(year_birth, year_death + 1)]

        if year_birth:
            return year_birth

        if year_death:
            return year_death

    def prepare_date_display(self, instance):
        date_birth = instance.date_birth
        date_death = instance.date_death

        if date_birth and date_death:
            return "{} – {}".format(str(date_birth), str(date_death))

        if date_birth:
            return "{} – ?".format(str(date_birth))

        if date_death:
            return "? – {}".format(str(date_death))


@registry.register_document
class OrganisationDocument(AgentDocument):
    members = get_agent_field()

    class Index:
        name = "rt-organisations"

    class Django:
        model = Organisation
