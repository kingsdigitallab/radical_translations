from django.db import models
from kdl_wagtail.core.models import BaseIndexPage, BasePage, BaseStreamPage, IndexPage
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.query import PageQuerySet


class BlogIndexPage(BaseIndexPage):
    subpage_types = ["BlogPost"]

    def children(self) -> PageQuerySet:
        return (
            BlogPost.objects.descendant_of(self).live().order_by("-first_published_at")
        )


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey("BlogPost", related_name="tagged_items")


class BlogPost(BaseStreamPage):
    guest_authors = models.CharField(max_length=256, blank=True, null=True)
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    parent_page_types = [BlogIndexPage]
    subpage_types = []

    @property
    def author(self) -> str:
        if self.guest_authors:
            return self.guest_authors

        if self.owner:
            return f"{self.owner.first_name} {self.owner.last_name}"

        return ""

    @property
    def index(self) -> IndexPage:
        return self.get_ancestors().type(IndexPage).last()

    promote_panels = BasePage.promote_panels + [
        FieldPanel("guest_authors"),
        FieldPanel("tags"),
    ]