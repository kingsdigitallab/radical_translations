# Generated by Django 2.2.10 on 2020-06-08 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_alter_unique_together_for_resource'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classification',
            name='source',
        ),
    ]
