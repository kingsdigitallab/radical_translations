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
    name = fields.TextField()
    based_near = get_place_field()
    roles = get_controlled_term_field()
    sources = get_resource_field()

    contributed_to = fields.ObjectField(
        properties={
            "resource": get_resource_field(),
            "roles": get_controlled_term_field(),
        }
    )

    class Index:
        name = "rt-agents"

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
    year_birth = fields.IntegerField()
    place_birth = get_place_field()
    year_death = fields.IntegerField()
    place_death = get_place_field()

    languages = get_controlled_term_field()

    knows = get_agent_field()
    member_of = get_agent_field()

    class Django:
        model = Person

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

    def prepare_year_birth(self, instance):
        db = instance.date_birth

        if db and db.date_earliest:
            if db.get_date_earliest() is not None:
                return db.get_date_earliest().year

    def prepare_year_death(self, instance):
        dd = instance.date_death

        if dd and dd.date_latest:
            if dd.get_date_latest() is not None:
                return dd.get_date_latest().year


@registry.register_document
class OrganisationDocument(AgentDocument):
    members = get_agent_field()

    class Django:
        model = Organisation
