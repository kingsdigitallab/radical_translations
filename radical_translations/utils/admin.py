from radical_translations.utils.models import Date
from django.contrib import admin


@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    fields = ["date_display"]
    search_fields = ["date_display"]
