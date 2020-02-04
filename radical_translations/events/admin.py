from django.contrib import admin

from radical_translations.events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    autocomplete_fields = ["date", "places", "related_to"]
    list_display = ["date", "places_display", "title"]
    search_fields = ["date", "places", "title"]

    def places_display(self, obj):
        return "; ".join([place.address for place in obj.places.all()])

    places_display.short_description = "Places"
