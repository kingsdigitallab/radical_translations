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
    list_display = ["name", "polymorphic_ctype"]
    list_filter = [PolymorphicChildModelFilter]
    search_fields = ["name"]


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
        "knows",
    ]
    inlines = AgentChildAdmin.inlines + [OrganisationInline]
