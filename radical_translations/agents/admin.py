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
    list_display = ["name", "agent_type", "roles_display", "based_near_display"]
    list_filter = [
        PolymorphicChildModelFilter,
        ("roles", admin.RelatedOnlyFieldListFilter),
        ("based_near", admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ["name"]

    def based_near_display(self, obj):
        return "; ".join([place.address for place in obj.based_near.all()])

    based_near_display.short_description = "Places"

    def roles_display(self, obj):
        return "; ".join([role.label for role in obj.roles.all()])

    roles_display.short_description = "Roles"


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
    autocomplete_fields = ["based_near"]
    inlines = [ContributionInline]
    search_fields = ["name"]
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
        "date_birth",
        "date_death",
        "place_birth",
        "place_death",
        "knows",
    ]
    inlines = AgentChildAdmin.inlines + [OrganisationInline]
