# Generated by Django 2.2.10 on 2021-01-21 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_merge_paratext_terms'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resourcerelationship',
            options={'ordering': ['related_to__date', 'relationship_type', 'resource__title']},
        ),
    ]
