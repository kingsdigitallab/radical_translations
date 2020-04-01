from django.contrib import admin
from geonames_place.admin import PlaceAdmin as GeonamesPlaceAdmin
from geonames_place.models import Place

from radical_translations.agents.admin import AgentInline
from radical_translations.events.admin import EventInline
from radical_translations.utils.models import Date


@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    fields = ["date_display", "date_radical"]
    search_fields = ["date_display", "date_radical"]


admin.site.unregister(Place)


@admin.register(Place)
class PlaceAdmin(GeonamesPlaceAdmin):
    inlines = [AgentInline, EventInline]
