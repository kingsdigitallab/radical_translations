from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from controlled_vocabulary.models import ControlledTerm
from geonames_place.models import Place
from radical_translations.agents.models import Agent
from radical_translations.core.models import Contribution
from radical_translations.utils.documents import (
    get_agent_field,
    get_controlled_term_field,
    get_place_field,
    get_resource_field,
)
from radical_translations.utils.models import Date


@registry.register_document
class AgentDocument(Document):
    meta = fields.KeywordField()

    agent_type = fields.KeywordField()
    name = fields.TextField(
        fields={
            "raw": fields.KeywordField(),
            "sort": fields.KeywordField(),
            "suggest": fields.CompletionField(),
        }
    )
    radical = fields.KeywordField()
    based_near = get_place_field()
    roles = get_controlled_term_field()
    sources = get_resource_field()

    contributed_to = fields.ObjectField(
        properties={
            "resource": get_resource_field(),
            "roles": get_controlled_term_field(),
        }
    )

    gender = fields.KeywordField()
    noble = fields.KeywordField()
    main_places = get_place_field()
    year = fields.IntegerField()
    date_display = fields.TextField()
    place_birth = get_place_field()
    place_death = get_place_field()
    languages = get_controlled_term_field()
    knows = get_agent_field()
    member_of = get_agent_field()

    members = get_agent_field()

    class Index:
        name = "rt-agents"

    class Django:
        model = Agent
        fields = ["id", "notes"]

    def get_queryset(self):
        return super().get_queryset().exclude(roles__label="library")

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Contribution):
            return related_instance.agent

        if isinstance(related_instance, Date):
            if related_instance.person_birth:
                return related_instance.person_birth

            return related_instance.person_death

        if isinstance(related_instance, (ControlledTerm, Place)):
            return related_instance.agents.all()

    def prepare_meta(self, instance):
        return [instance.agent_type]

    def prepare_radical(self, instance):
        return "yes" if instance.radical else "no"

    def prepare_gender(self, instance):
        if instance.is_person:
            return instance.get_gender_display()

    def prepare_noble(self, instance):
        if instance.is_person:
            return "yes" if instance.noble else "no"

    def prepare_main_places(self, instance):
        if instance.is_organisation:
            return

        return [self._prepare_place(place) for place in instance.main_places.all()]

    def _prepare_place(self, place):
        if not place:
            return {}

        return {
            "address": place.address,
            "geo": place.geo,
            "coutry": {"name": place.country.name} if place.country else {},
        }

    def prepare_year(self, instance):
        if instance.is_organisation:
            return

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
        if instance.is_organisation:
            return

        date_birth = instance.date_birth
        date_death = instance.date_death

        if date_birth and date_death:
            return "{} – {}".format(str(date_birth), str(date_death))

        if date_birth:
            return "{} – ?".format(str(date_birth))

        if date_death:
            return "? – {}".format(str(date_death))

    def prepare_place_birth(self, instance):
        if instance.is_person:
            return self._prepare_place(instance.place_birth)

    def prepare_place_death(self, instance):
        if instance.is_person:
            return self._prepare_place(instance.place_death)

    def prepare_languages(self, instance):
        if instance.is_organisation:
            return

        return [{"label": language.label} for language in instance.languages.all()]

    def prepare_knows(self, instance):
        if instance.is_organisation:
            return

        return [self._prepare_agent(person) for person in instance.knows.all()]

    def _prepare_agent(self, agent):
        if not agent:
            return {}

        return {"id": agent.id, "name": agent.name}

    def prepare_member_of(self, instance):
        if instance.is_organisation:
            return

        return [self._prepare_agent(org) for org in instance.member_of.all()]

    def prepare_members(self, instance):
        if instance.is_person:
            return

        return [self._prepare_agent(person) for person in instance.members.all()]
