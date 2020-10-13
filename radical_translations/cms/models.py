from django.conf import settings
from django.db import models
from kdl_wagtail.core.models import (
    BaseIndexPage,
    BasePage,
    BaseRichTextPage,
    BaseStreamPage,
    IndexPage,
)
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.core.query import PageQuerySet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from radical_translations.agents.models import Person


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


class HomePage(BasePage):
    features = settings.HOMEPAGE_RICHTEXT_FEATURES

    introduction = RichTextField(features=features)
    body = StreamField(
        blocks.StreamBlock(
            [
                (
                    "section",
                    blocks.StructBlock(
                        [
                            ("title", blocks.CharBlock()),
                            ("page", blocks.PageChooserBlock(can_choose_root=False)),
                            ("description", blocks.RichTextBlock(features=features)),
                        ],
                        icon="doc-full-inverse",
                    ),
                ),
                (
                    "featured",
                    blocks.StructBlock(
                        [
                            ("title", blocks.CharBlock()),
                            ("page", blocks.PageChooserBlock(can_choose_root=False)),
                            ("description", blocks.RichTextBlock(features=features)),
                        ],
                        icon="pick",
                    ),
                ),
            ],
            block_counts={
                "section": {"min_number": 4, "max_num": 4},
                "featured": {"min_number": 3, "max_num": 3},
            },
        )
    )

    subpage_types = [
        "kdl_wagtail_zotero.BibliographyIndexPage",
        "BlogIndexPage",
        "kdl_wagtail_core.ContactUsPage",
        "kdl_wagtail_core.IndexPage",
        "kdl_wagtail_people.PeopleIndexPage",
        "kdl_wagtail_core.RichTextPage",
        "kdl_wagtail_core.SitemapPage",
        "kdl_wagtail_core.StreamPage",
    ]

    content_panels = Page.content_panels + [
        FieldPanel("introduction", classname="full"),
        StreamFieldPanel("body"),
    ]


register_snippet(Person)


class BiographyPage(BaseRichTextPage):
    person = models.ForeignKey(
        Person,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="biographies",
    )

    content_panels = BasePage.content_panels + [
        SnippetChooserPanel("person"),
        FieldPanel("body", classname="full"),
    ]
