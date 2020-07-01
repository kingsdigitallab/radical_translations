# Generated by Django 2.2.10 on 2020-07-01 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geonames_place", "0004_change_meta_options_on_country"),
        ("agents", "0008_alter_field_page_on_agent"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="main_places",
            field=models.ManyToManyField(
                blank=True,
                help_text="Main places this Person is associated with (places of residence, etc).",
                related_name="agents_main_places",
                to="geonames_place.Place",
            ),
        ),
    ]
