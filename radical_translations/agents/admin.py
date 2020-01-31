from django.contrib import admin
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicParentModelAdmin,
)

from radical_translations.agents.models import Agent, Organisation, Person


@admin.register(Agent)
class AgentAdmin(PolymorphicParentModelAdmin):
    child_models = [Organisation, Person]
    list_display = ["name", "polymorphic_ctype"]
    list_filter = [PolymorphicChildModelFilter]
    search_fields = ["name"]


class AgentChildAdmin(PolymorphicChildModelAdmin):
    autocomplete_fields = ["based_near"]
    search_fields = ["name"]
    show_in_index = True


@admin.register(Organisation)
class OrganisationAdmin(AgentChildAdmin):
    autocomplete_fields = AgentChildAdmin.autocomplete_fields + ["members"]


@admin.register(Person)
class PersonAdmin(AgentChildAdmin):
    autocomplete_fields = AgentChildAdmin.autocomplete_fields + [
        "date_birth",
        "date_death",
        "knows",
    ]
