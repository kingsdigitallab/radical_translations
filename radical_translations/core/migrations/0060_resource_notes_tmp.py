# Generated by Django 2.2.28 on 2023-03-16 17:19

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0059_change_meta_ordering_on_resource'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='notes_tmp',
            field=markdownx.models.MarkdownxField(blank=True, help_text='Information, usually in textual form, on attributes of a resource or some aspect of a resource.', null=True),
        ),
    ]
