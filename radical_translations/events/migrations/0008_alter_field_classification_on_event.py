# Generated by Django 2.2.10 on 2020-05-05 14:39

import controlled_vocabulary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_event_classification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='classification',
            field=controlled_vocabulary.models.ControlledTermsField(blank=True, help_text='Editorial classification.', related_name='_event_classification_+', to='controlled_vocabulary.ControlledTerm', vocabularies=['wikidata']),
        ),
    ]
