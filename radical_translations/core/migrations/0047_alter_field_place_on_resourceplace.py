# Generated by Django 2.2.10 on 2020-07-30 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_role_author_to_translator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourceplace',
            name='place',
            field=models.ForeignKey(blank=True, help_text='Geographic location or place entity associated with a resource or element of description, such as the place associated with the publication, printing, distribution, issue, release or production of a resource, place of an event.', null=True, on_delete=django.db.models.deletion.CASCADE, to='geonames_place.Place'),
        ),
    ]