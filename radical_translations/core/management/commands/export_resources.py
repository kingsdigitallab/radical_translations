import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from radical_translations.core.models import Resource


class Command(BaseCommand):
    help = "Exports `Resource` data into a CSV file."

    def handle(self, *args, **options):
        self.stdout.write(
            "Exporting Resources into CSV file resources.csv ...", ending=" "
        )
        resources = [resource.to_dict() for resource in Resource.objects.all()]

        if not resources:
            self.stderr.write(self.style.NOTICE("No resources found!"))
            return -1

        fieldnames = resources[0].keys()

        with open(os.path.join(settings.EXPORTS_ROOT, "resources.csv"), "w") as f:
            c = csv.DictWriter(f, fieldnames)
            c.writeheader()
            c.writerows(resources)

        self.stdout.write(self.style.SUCCESS("done"))
