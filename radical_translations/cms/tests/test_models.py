import pytest

from radical_translations.cms.models import BlogIndexPage, BlogPost

pytestmark = pytest.mark.django_db


class TestBlogIndexPage:
    @pytest.mark.usefixtures("blog_index_page", "blog_post_1", "blog_post_2")
    def test_children(
        self,
        blog_index_page: BlogIndexPage,
        blog_post_1: BlogPost,
        blog_post_2: BlogPost,
    ):
        children = blog_index_page.children()

        assert children is not None
        assert children.count() == 2

        blog_post_2.unpublish()
        children = blog_index_page.children()
        assert children.count() == 1


@pytest.mark.usefixtures("blog_index_page")
class TestBlogPost:
    @pytest.mark.usefixtures("blog_index_page", "blog_post_1")
    def test_author(self, blog_post_1: BlogPost):
        assert blog_post_1.author is not None
        assert blog_post_1.author == ""

        blog_post_1.guest_authors = "Guest"
        assert blog_post_1.author == blog_post_1.guest_authors

        blog_post_1.guest_authors = None
        blog_post_1.owner = None
        assert blog_post_1.author == ""
