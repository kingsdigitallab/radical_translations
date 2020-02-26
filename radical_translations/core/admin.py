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

    def get_model_perms(self, req):
        return {}


@admin.register(Resource)
class ResourceAdmin(PolymorphicParentModelAdmin):
    child_models = [Work, Instance, Item]
    list_display = ["title", "get_language_names", "polymorphic_ctype"]
    list_filter = [
        PolymorphicChildModelFilter,
        ("relationships__relationship_type", admin.RelatedOnlyFieldListFilter),
        ("classifications__edition", admin.RelatedOnlyFieldListFilter),
        ("subjects", admin.RelatedOnlyFieldListFilter),
        ("languages", admin.RelatedOnlyFieldListFilter),
        ("places", admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = [
        "title__main_title",
        "title__subtitle",
        "title_variant__main_title",
        "title_variant__subtitle",
    ]


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


@admin.register(Work)
class WorkAdmin(ResourceChildAdmin):
    pass


@admin.register(Instance)
class InstanceAdmin(ResourceChildAdmin):
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        obj = form.instance
        obj.refresh_from_db()

        if obj.relationships.count() == 0 and not obj.instance_of():
            Work.from_instance(obj)


@admin.register(Item)
class ItemAdmin(ResourceChildAdmin):
    pass
