# Generated by Django 2.2.10 on 2020-05-04 09:59

import controlled_vocabulary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0018_resourcerelationship_classification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resource",
            name="subjects",
            field=controlled_vocabulary.models.ControlledTermsField(
                blank=True,
                help_text="Subject term(s) describing a resource",
                related_name="_resource_subjects_+",
                to="controlled_vocabulary.ControlledTerm",
                vocabularies=["fast-topic", "fast-forms", "wikidata"],
            ),
        ),
    ]