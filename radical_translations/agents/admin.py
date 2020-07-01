from django.contrib import admin
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicParentModelAdmin,
)

from radical_translations.agents.models import Agent, Organisation, Person
from radical_translations.core.models import Contribution


@admin.register(Agent)
class AgentAdmin(PolymorphicParentModelAdmin):
    child_models = [Organisation, Person]
    list_display = ["name", "agent_type", "get_role_names", "get_place_names"]
    list_filter = [
        PolymorphicChildModelFilter,
        ("roles", admin.RelatedOnlyFieldListFilter),
        ("based_near", admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ["name", "roles__label", "based_near__address"]


class AgentInline(admin.TabularInline):
    model = Agent.based_near.through
    autocomplete_fields = ["agent"]
    extra = 1
    fk_name = "place"
    readonly_fields = ["place"]


class ContributionInline(admin.TabularInline):
    model = Contribution
    autocomplete_fields = ["resource"]
    extra = 1
    fk_field = "contributed_to"


class AgentChildAdmin(PolymorphicChildModelAdmin):
    autocomplete_fields = ["based_near", "sources"]
    inlines = [ContributionInline]
    list_display = ["name", "get_role_names", "get_place_names"]
    list_filter = [
        ("roles", admin.RelatedOnlyFieldListFilter),
        ("based_near", admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ["name", "roles__label", "based_near__address"]
    show_in_index = True


@admin.register(Organisation)
class OrganisationAdmin(AgentChildAdmin):
    autocomplete_fields = AgentChildAdmin.autocomplete_fields + ["members"]


class OrganisationInline(admin.TabularInline):
    model = Organisation.member_of.through
    autocomplete_fields = ["organisation"]
    extra = 1
    verbose_name = "Organisation"
    verbose_name_plural = "Organisations"


@admin.register(Person)
class PersonAdmin(AgentChildAdmin):
    autocomplete_fields = AgentChildAdmin.autocomplete_fields + [
        "main_places",
        "date_birth",
        "date_death",
        "place_birth",
        "place_death",
        "knows",
    ]
    inlines = AgentChildAdmin.inlines + [OrganisationInline]
    list_display = [
        "name",
        "gender",
        "date_birth",
        "place_birth",
        "date_death",
        "place_death",
        "get_role_names",
        "get_main_places_names",
        "get_place_names",
    ]
    list_filter = [
        "gender",
        ("roles", admin.RelatedOnlyFieldListFilter),
        ("languages", admin.RelatedOnlyFieldListFilter),
        ("main_places", admin.RelatedOnlyFieldListFilter),
        ("based_near", admin.RelatedOnlyFieldListFilter),
        ("knows", admin.RelatedOnlyFieldListFilter),
    ]
