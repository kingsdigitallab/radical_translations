from django.core.management.base import BaseCommand
from urllib import request
import json
from radical_translations.events.models import Event


class Command(BaseCommand):
    help = "Imports data from a data collection spreadsheet"

    def add_arguments(self, parser):
        parser.add_argument(
            "url", nargs=1, type=str, help="The URL to the Events JSON file."
        )
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
                self.stdout.write(self.style.WARNING("Deleting all events..."))
                Event.objects.all().delete()

            self.stdout.write("Importing events...")
            for entry in entries:
                event = Event.from_gsx_entry(entry)
                self.stdout.write(self.style.SUCCESS(f"- {event}"))
