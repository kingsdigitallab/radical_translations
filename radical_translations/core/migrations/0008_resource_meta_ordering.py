# Generated by Django 2.2.9 on 2020-02-10 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_title_main_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resource',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['main_title', 'subtitle']},
        ),
    ]
