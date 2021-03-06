# Generated by Django 2.2.10 on 2020-10-13 13:07

from django.db import migrations
from kdl_wagtail.core.utils import migrate_wagtail_page_type


def get_queryset(apps, qs):
    IndexPage = apps.get_model("kdl_wagtail_core", "IndexPage")

    try:
        biographies = IndexPage.objects.get(title="Biographies")
        return qs.filter(path__startswith=biographies.path)
    except IndexPage.DoesNotExist:
        return qs.none()


def get_richtextpage():
    return ("kdl_wagtail_core", "RichTextPage")


def get_biographypage():
    return ("cms", "BiographyPage")


def convert_to_biographypage(apps, schema_editor):
    def select(qs):
        return get_queryset(apps, qs)

    mapping = {
        "models": {
            "from": get_richtextpage(),
            "to": get_biographypage(),
        },
        "select": select,
    }

    migrate_wagtail_page_type(apps, schema_editor, mapping)


def convert_to_richtextpage(apps, schema_editor):
    def select(qs):
        return get_queryset(apps, qs)

    mapping = {
        "models": {
            "from": get_biographypage(),
            "to": get_richtextpage(),
        },
        "select": select,
    }

    migrate_wagtail_page_type(apps, schema_editor, mapping)


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0005_biographypage"),
        ("kdl_wagtail_core", "0020_contactusfield_clean_name"),
    ]

    operations = [
        migrations.RunPython(
            convert_to_biographypage,
            reverse_code=convert_to_richtextpage,
        ),
    ]
