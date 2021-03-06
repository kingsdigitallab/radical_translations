# Generated by Django 2.2.10 on 2020-09-15 12:52

from django.db import migrations

from controlled_vocabulary.utils import search_term_or_none


def fast_topic_to_fast_forms(apps, schema_editor):
    ControlledTerm = apps.get_model("controlled_vocabulary", "ControlledTerm")
    Resource = apps.get_model("core", "Resource")

    term = search_term_or_none("fast-topic", "essays")
    essays_ft = ControlledTerm.objects.get(id=term.id)

    term = search_term_or_none("fast-forms", "essays")
    essays_ff = ControlledTerm.objects.get(id=term.id)

    for resource in Resource.objects.filter(subjects=essays_ft):
        resource.subjects.remove(essays_ft)
        resource.subjects.add(essays_ff)
        resource.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0048_resourceplace_fictional_place"),
    ]

    operations = [
        migrations.RunPython(
            fast_topic_to_fast_forms, reverse_code=migrations.RunPython.noop
        )
    ]
