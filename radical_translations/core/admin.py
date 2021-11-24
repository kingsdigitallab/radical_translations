from django.contrib import admin

from radical_translations.core.models import (
    Classification,
    Contribution,
    Resource,
    ResourceLanguage,
    ResourcePlace,
    ResourceRelationship,
    Title,
)
from radical_translations.events.models import Event


class ClassificationInline(admin.TabularInline):
    model = Classification
    autocomplete_fields = ["classification"]
    extra = 1
    fk_name = "resource"


class ContributionInline(admin.TabularInline):
    model = Contribution
    autocomplete_fields = ["agent"]
    extra = 1
    fk_name = "resource"


class EventInline(admin.TabularInline):
    model = Event.related_to.through
    autocomplete_fields = ["event"]
    extra = 1
    verbose_name = "Event related to this resource"
    verbose_name_plural = "Events related to this resource"


class ResourceLanguageInline(admin.TabularInline):
    model = ResourceLanguage
    extra = 1
    verbose_name = "Language"
    verbose_name_plural = "Languages"


class ResourcePlaceInline(admin.TabularInline):
    model = ResourcePlace
    autocomplete_fields = ["place"]
    extra = 1
    verbose_name = "Place"
    verbose_name_plural = "Places"


class ResourceRelationshipInline(admin.TabularInline):
    model = ResourceRelationship
    autocomplete_fields = ["relationship_type", "related_to"]
    extra = 1
    fk_name = "resource"
    verbose_name = "Relationship from this resource"
    verbose_name_plural = "Relationships from this resource"


class ResourceRelationshipInverseInline(admin.TabularInline):
    model = ResourceRelationship
    autocomplete_fields = ["resource", "relationship_type"]
    extra = 1
    fk_name = "related_to"
    verbose_name = "Relationship to this resource"
    verbose_name_plural = "Relationships to this resource"


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ["main_title", "subtitle"]
    search_fields = ["main_title", "subtitle"]


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        "date",
        "subjects",
        "held_by",
        "title",
        "title_variant",
    ]
    # empty_value_display = "unknown"
    inlines = [
        ClassificationInline,
        ContributionInline,
        ResourceLanguageInline,
        ResourcePlaceInline,
        ResourceRelationshipInline,
        ResourceRelationshipInverseInline,
        EventInline,
    ]
    list_display = [
        "title",
        "date",
        "is_private",
        "is_original",
        "is_paratext",
        "get_authors",
        "get_classification_edition",
        "get_language_names",
        "get_place_names",
    ]
    list_filter = [
        ("relationships__relationship_type", admin.RelatedOnlyFieldListFilter),
        ("classifications__edition", admin.RelatedOnlyFieldListFilter),
        ("subjects", admin.RelatedOnlyFieldListFilter),
        ("contributions__roles", admin.RelatedOnlyFieldListFilter),
        ("languages__language", admin.RelatedOnlyFieldListFilter),
        ("places__place", admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = [
        "title__main_title",
        "title__subtitle",
        "title_variant__main_title",
        "title_variant__subtitle",
    ]

    class Media:
        css = {"all": ("css/admin.css",)}
