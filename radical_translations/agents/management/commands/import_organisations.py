from django.core.management.base import BaseCommand
from urllib import request
import json
from radical_translations.agents.models import Organisation


class Command(BaseCommand):
    help = "Imports `Organisation`s data from a data collection spreadsheet."

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
                self.stdout.write(self.style.WARNING("Deleting all organisations..."))
                Organisation.objects.all().delete()

            self.stdout.write("Importing organisations...")
            for entry in entries:
                org = Organisation.from_gsx_entry(entry)
                self.stdout.write(self.style.SUCCESS(f"- {org}"))
