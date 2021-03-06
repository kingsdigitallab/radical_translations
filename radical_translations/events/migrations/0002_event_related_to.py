# Generated by Django 2.2.9 on 2020-02-04 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_help_text"),
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="related_to",
            field=models.ManyToManyField(
                blank=True,
                help_text="Resources that are related to this  Event.",
                to="core.Resource",
            ),
        ),
    ]
