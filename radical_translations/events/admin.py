from django.contrib import admin
from radical_translations.events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    autocomplete_fields = ["date", "place", "related_to"]
    list_display = ["date", "place", "title"]
    list_filter = [("place", admin.RelatedOnlyFieldListFilter)]
    search_fields = ["date", "place", "title"]


class EventInline(admin.TabularInline):
    model = Event
    autocomplete_fields = EventAdmin.autocomplete_fields
    extra = 1
