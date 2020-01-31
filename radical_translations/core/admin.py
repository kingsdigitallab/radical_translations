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
    Note,
    Resource,
    ResourceRelationship,
    Role,
    Source,
    Title,
    Work,
)


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    autocomplete_fields = ["source"]
    search_fields = ["edition"]


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    autocomplete_fields = ["role", "notes"]
    search_fields = ["agent", "role"]


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    search_fields = ["note"]


@admin.register(ResourceRelationship)
class ResourceRelationshipAdmin(admin.ModelAdmin):
    autocomplete_fields = ["resource", "relationship_type", "related_to"]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    search_fields = ["role"]


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    search_fields = ["source"]


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    autocomplete_fields = ["notes"]
    search_fields = ["title", "notes"]


@admin.register(Resource)
class ResourceAdmin(PolymorphicParentModelAdmin):
    child_models = [Work, Instance, Item]
    list_display = ["title", "polymorphic_ctype"]
    list_filter = [PolymorphicChildModelFilter]
    search_fields = ["title"]


class ResourceRelationshipInline(admin.TabularInline):
    model = ResourceRelationship
    autocomplete_fields = ["relationship_type", "related_to"]
    extra = 1
    fk_name = "resource"


class ResourceChildAdmin(PolymorphicChildModelAdmin):
    autocomplete_fields = [
        "languages",
        "classifications",
        "notes",
        "subjects",
        "title",
    ]
    inlines = [ResourceRelationshipInline]
    search_fields = ["title"]
    show_in_index = True


@admin.register(Work)
class WorkAdmin(ResourceChildAdmin):
    autocomplete_fields = ResourceChildAdmin.autocomplete_fields + [
        "contributions",
        "origin_date",
    ]


@admin.register(Instance)
class InstanceAdmin(ResourceChildAdmin):
    autocomplete_fields = ResourceChildAdmin.autocomplete_fields + ["contributions"]


@admin.register(Item)
class ItemAdmin(ResourceChildAdmin):
    pass
