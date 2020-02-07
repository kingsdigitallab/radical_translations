from django.contrib import admin
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicParentModelAdmin,
)

from radical_translations.core.models import (
    Classification,
    Contribution,
    Instance,
    Item,
    Resource,
    ResourceRelationship,
    Title,
    Work,
)
from radical_translations.events.models import Event


class ClassificationInline(admin.TabularInline):
    model = Classification
    autocomplete_fields = ["source"]
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
    search_fields = ["title", "subtitle"]


@admin.register(Resource)
class ResourceAdmin(PolymorphicParentModelAdmin):
    child_models = [Work, Instance, Item]
    list_display = ["title", "date", "polymorphic_ctype"]
    list_filter = [
        PolymorphicChildModelFilter,
        ("places", admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ["title", "title_variant"]


class ResourceChildAdmin(PolymorphicChildModelAdmin):
    autocomplete_fields = [
        "date",
        "languages",
        "places",
        "subjects",
        "title",
        "title_variant",
    ]
    inlines = [
        ClassificationInline,
        ContributionInline,
        ResourceRelationshipInline,
        ResourceRelationshipInverseInline,
        EventInline,
    ]
    list_display = ["title", "date"]
    search_fields = ["title", "title_variant"]
    show_in_index = True


@admin.register(Work)
class WorkAdmin(ResourceChildAdmin):
    pass


@admin.register(Instance)
class InstanceAdmin(ResourceChildAdmin):
    pass


@admin.register(Item)
class ItemAdmin(ResourceChildAdmin):
    pass
