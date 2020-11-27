# Generated by Django 2.2.10 on 2020-11-27 11:15

from django.db import migrations


def merge_languages(apps, schema_editor):
    ControlledTerm = apps.get_model("controlled_vocabulary", "ControlledTerm")

    try:
        fra = ControlledTerm.objects.get(termid="fra", label="French")
        fre = ControlledTerm.objects.get(termid="fre", label="French")
    except ControlledTerm.DoesNotExist:
        return

    ResourceLanguage = apps.get_model("core", "ResourceLanguage")
    for rl in ResourceLanguage.objects.filter(language=fra):
        rl.language = fre
        rl.save()

    Person = apps.get_model("agents", "Person")
    for p in Person.objects.filter(languages=fra):
        p.languages.remove(fra)
        p.languages.add(fre)
        p.save()

    fra.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("utils", "0007_unload_date_radical"),
    ]

    operations = [
        migrations.RunPython(merge_languages, reverse_code=migrations.RunPython.noop)
    ]