import json
from urllib import request

from django.core.management.base import BaseCommand

from radical_translations.core.models import Resource


class Command(BaseCommand):
    help = "Imports `Resource` data from a data collection spreadsheet."

    def add_arguments(self, parser):
        parser.add_argument("url", nargs=1, type=str, help="The URL to the JSON file.")
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete existing data before importing",
        )

    def handle(self, *args, **options):
        url = options["url"][0]
        delete = options["delete"]

        with request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            entries = data["feed"]["entry"]

            if delete:
                self.stdout.write(self.style.WARNING("Deleting all resources..."))
                Resource.objects.all().delete()

            self.stdout.write("Importing resources...")
            for entry in entries:
                resource = Resource.from_gsx_entry(entry)
                if resource:
                    self.stdout.write(self.style.SUCCESS(f"- {resource}"))
