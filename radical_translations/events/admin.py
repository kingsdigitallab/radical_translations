from django.contrib import admin

from radical_translations.events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
