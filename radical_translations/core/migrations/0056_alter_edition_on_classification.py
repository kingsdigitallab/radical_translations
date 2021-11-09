# Generated by Django 2.2.10 on 2021-07-08 14:20

import controlled_vocabulary.models
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_paratext_functions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classification',
            options={'ordering': ['edition__vocabulary', 'edition__label']},
        ),
        migrations.AlterField(
            model_name='classification',
            name='edition',
            field=controlled_vocabulary.models.ControlledTermField(help_text='Edition of the classification scheme, such as full, abridged or a number, when a classification scheme designates editions.', on_delete=django.db.models.deletion.CASCADE, related_name='classifications', to='controlled_vocabulary.ControlledTerm', vocabularies=['rt-ppt', 'rt-tt', 'rt-pt', 'rt-ptf']),
        ),
    ]