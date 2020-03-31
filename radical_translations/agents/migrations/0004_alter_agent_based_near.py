# Generated by Django 2.2.10 on 2020-03-04 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0003_alter_agent_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='based_near',
            field=models.ManyToManyField(blank=True, help_text='A location that something is based near, for some broadly human notion of near.', related_name='agents', to='geonames_place.Place'),
        ),
    ]