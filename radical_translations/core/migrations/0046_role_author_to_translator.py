# Generated by Django 2.2.10 on 2020-07-22 08:35

from django.db import migrations

from controlled_vocabulary.utils import search_term_or_none


def load_translator(apps, schema_editor):
    Contribution = apps.get_model("core", "Contribution")
    ControlledTerm = apps.get_model("controlled_vocabulary", "ControlledTerm")

    term = search_term_or_none("wikidata", "author")
    author = ControlledTerm.objects.get(id=term.id)

    term = search_term_or_none("wikidata", "translator")
    translator = ControlledTerm.objects.get(id=term.id)

    for c in Contribution.objects.filter(roles__label=author.label):
        if (
            c.resource.relationships.filter(
                relationship_type__label="translation of"
            ).count()
            > 0
        ):
            c.roles.add(translator)
            c.roles.remove(author)
            c.save()


def unload_translator(apps, schema_editor):
    Contribution = apps.get_model("core", "Contribution")
    ControlledTerm = apps.get_model("controlled_vocabulary", "ControlledTerm")

    term = search_term_or_none("wikidata", "author")
    author = ControlledTerm.objects.get(id=term.id)

    term = search_term_or_none("wikidata", "translator")
    translator = ControlledTerm.objects.get(id=term.id)

    for c in Contribution.objects.filter(roles__label=translator.label):
        c.roles.add(author)
        c.roles.remove(translator)
        c.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0045_classification_classification"),
    ]

    operations = [migrations.RunPython(load_translator, reverse_code=unload_translator)]