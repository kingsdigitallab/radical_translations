# Generated by Django 2.2.10 on 2020-05-18 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0004_date_editorialclassification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='date_display',
            field=models.CharField(help_text='Date in EDTF format: https://www.loc.gov/standards/datetime/', max_length=255),
        ),
    ]
