from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from geonames_place.admin import PlaceAdmin as GeonamesPlaceAdmin
from geonames_place.models import Place

from radical_translations.agents.admin import AgentInline
from radical_translations.events.admin import EventInline
from radical_translations.utils.models import Date


@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    fields = [
        "date_display",
        "date_display_classification",
        "date_radical",
        "date_radical_classification",
    ]
    list_display = ['date_display', 'date_radical']
    search_fields = ["date_display", "date_radical"]


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """Log Entry admin interface."""
    date_hierarchy = 'action_time'
    fields = (
        'action_time', 'user', 'content_type', 'object_id',
        'object_repr', 'action_flag', 'change_message',
    )
    list_display = (
        'action_time', 'user', 'action_message', 'content_type', 'object_link',
    )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        'action_flag', 'content_type',
    )
    search_fields = (
        'object_repr', 'change_message',
    )

    def object_link(self, obj):
        """Returns the admin link to the log entry object if it exists."""
        admin_url = None if obj.is_deletion() else obj.get_admin_url()
        if admin_url:
            return format_html('<a href="{}">{}</a>', admin_url, obj.object_repr)
        else:
            return obj.object_repr

    object_link.short_description = 'object'

    def action_message(self, obj):
        """
        Returns the action message.
        Note: this handles deletions which don't return a change message.
        """
        change_message = obj.get_change_message()
        # If there is no change message then use the action flag label
        if not change_message:
            change_message = '{}.'.format(obj.get_action_flag_display())
        return change_message

    action_message.short_description = 'action'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('content_type')

    def has_add_permission(self, request):
        """Log entries cannot be added manually."""
        return False

    def has_change_permission(self, request, obj=None):
        """Log entries cannot be changed."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Log entries can only be deleted when the setting is enabled."""
        return False

    # Prevent changes to log entries creating their own log entries!
    def log_addition(self, request, object, message):
        pass

    def log_change(self, request, object, message):
        pass

    def log_deletion(self, request, object, object_repr):
        pass


admin.site.unregister(Place)


@admin.register(Place)
class PlaceAdmin(GeonamesPlaceAdmin):
    inlines = [AgentInline, EventInline]
