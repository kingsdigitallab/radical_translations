# Generated by Django 2.2.10 on 2020-02-26 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0002_agent_meta_ordering'),
        ('core', '0010_alter_resourcerelationship_related_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='electronic_locator',
            field=models.URLField(blank=True, help_text='Electronic location from which the resource is available.', max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='held_by',
            field=models.ForeignKey(blank=True, help_text='Entity holding the item or from which it is available.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='agents.Agent'),
        ),
    ]