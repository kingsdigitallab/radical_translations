# Generated by Django 2.2.10 on 2020-06-08 14:00

import controlled_vocabulary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controlled_vocabulary', '0004_remove_controlledvocabulary_test'),
        ('core', '0044_remove_classification_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='classification',
            name='classification',
            field=controlled_vocabulary.models.ControlledTermsField(blank=True, help_text='Editorial classification.', related_name='_classification_classification_+', to='controlled_vocabulary.ControlledTerm', vocabularies=['wikidata']),
        ),
    ]