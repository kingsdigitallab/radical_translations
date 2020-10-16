from django import template
from wagtail.core.models import Page

register = template.Library()


@register.inclusion_tag("cms/tags/breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    page = context.get("self")

    # on the home page
    if page is None or page.depth <= 2:
        # no need for breadcrumbs
        return {"ancestors": []}

    return {
        "ancestors": Page.objects.ancestor_of(page, inclusive=True).filter(depth__gt=2)
    }
