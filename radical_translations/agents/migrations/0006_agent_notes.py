# Generated by Django 2.2.10 on 2020-06-02 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0005_add_person_place_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='notes',
            field=models.TextField(blank=True, help_text='Information, usually in textual form, on attributes of an agent or some aspect of an agent.', null=True),
        ),
    ]
