# Generated by Django 2.2.10 on 2020-05-27 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0005_alter_date_display_on_date'),
        ('core', '0042_update_vocabularies_on_classification_and_resource'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together={('title', 'date', '_is_paratext')},
        ),
    ]
