from django import template
from markdownx.utils import markdownify
from wagtail.core.models import Page

register = template.Library()


@register.inclusion_tag("cms/tags/breadcrumbs.html", takes_context=True)
def breadcrumbs(context) -> dict:
    page = context.get("self")

    # not on a wagtail page
    if page is None:
        return {"ancestors": [], "crumbs": get_object_crumbs(context)}

    # on the home page
    if page.depth <= 2:
        return {"ancestors": []}

    return {
        "ancestors": Page.objects.ancestor_of(page, inclusive=True).filter(depth__gt=2)
    }


def get_object_crumbs(context) -> list:
    crumbs = []

    path = context.request.path
    parts = path.split("/")[1:-1]
    parts_count = len(parts)

    for item in parts[:-1]:
        parts_count -= 1
        crumbs.append({"path": "../" * parts_count, "title": item.title()})

    last_crumb = {"path": "#", "title": parts[-1].title()}

    obj = context.get("object")
    if obj:
        last_crumb["title"] = getattr(obj, "title", str(obj))

    crumbs.append(last_crumb)

    return crumbs


@register.filter()
def md(content):
    return markdownify(content)
