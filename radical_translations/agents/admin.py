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


@admin.register(Person)
class PersonAdmin(AgentChildAdmin):
    autocomplete_fields = AgentChildAdmin.autocomplete_fields + [
        "date_birth",
        "date_death",
        "knows",
    ]

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        return fields + ["member_of"]
