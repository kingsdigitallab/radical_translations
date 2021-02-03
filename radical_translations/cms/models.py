from django.conf import settings
from django.db import models
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Site
from wagtail.core.query import PageQuerySet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from kdl_wagtail.core.models import (
    BaseIndexPage,
    BasePage,
    BaseRichTextPage,
    BaseStreamPage,
    IndexPage,
)
from radical_translations.agents.models import Person
from radical_translations.core.models import Resource


class BlogIndexPage(RoutablePageMixin, BaseIndexPage):
    subpage_types = ["BlogPost"]

    def children(self) -> PageQuerySet:
        return (
            BlogPost.objects.descendant_of(self).live().order_by("-first_published_at")
        )

    @route(r"^$")
    def all_posts(self, request):
        return render(
            request, self.get_template(request), {"children": self.children()}
        )

    @route(r"^tag/")
    @route(r"^tag/(?P<tag>[\w\s\-]+)/$", name="posts_by_tag")
    def posts_by_tag(self, request, tag=None):
        if not tag:
            return self.all_posts(request)

        posts = self.children().filter(tags__slug=tag)

        return render(
            request,
            self.get_template(request),
            {"page": self, "children": posts, "filter_type": "tag", "filter": tag},
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
            if self.owner.name:
                return self.owner.name

            return self.owner.get_full_name() or self.owner.get_username()

        return None

    @property
    def index(self) -> IndexPage:
        return self.get_ancestors().type(IndexPage).last()

    promote_panels = BasePage.promote_panels + [
        FieldPanel("guest_authors"),
        FieldPanel("tags"),
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

    def get_url(self, request: HttpRequest = None, current_site: Site = None):
        if self.person:
            return reverse("agent-detail", kwargs={"pk": self.person.id})

        return super().get_url(request=request, current_site=current_site)


register_snippet(Resource)


class HomePage(BasePage):
    features = settings.HOMEPAGE_RICHTEXT_FEATURES

    introduction = RichTextField(features=features)

    sections = StreamField(
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
            ],
            block_counts={
                "section": settings.HOMEPAGE_SECTION_BLOCK_COUNTS,
            },
        )
    )

    featured_biography = models.ForeignKey(
        BiographyPage,
        # default=BiographyPage.objects.order_by("-modified").first(),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    featured_resource = models.ForeignKey(
        Resource, blank=True, null=True, on_delete=models.SET_NULL, related_name="+"
    )
    featured_blog_post = models.ForeignKey(
        BlogPost, blank=True, null=True, on_delete=models.SET_NULL, related_name="+"
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
        StreamFieldPanel("sections"),
        PageChooserPanel("featured_biography"),
        SnippetChooserPanel("featured_resource"),
        PageChooserPanel("featured_blog_post"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.id:
            self.featured_biography = (
                BiographyPage.objects.live().order_by("-last_published_at").first()
            )
            self.featured_resource = Resource.objects.order_by("-modified").first()
            self.featured_blog_post = (
                BlogPost.objects.live().order_by("-last_published_at").first()
            )
