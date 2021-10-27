import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from radical_translations.events.models import Event


class Command(BaseCommand):
    help = "Exports `Event` data into a CSV file."

    def handle(self, *args, **options):
        self.stdout.write("Exporting Events into CSV file events.csv ...", ending=" ")
        events = [event.to_dict() for event in Event.objects.all()]

        if not events:
            self.stderr.write(self.style.NOTICE("No events found!"))
            return -1

        fieldnames = events[0].keys()

        with open(os.path.join(settings.EXPORTS_ROOT, "events.csv"), "w") as f:
            c = csv.DictWriter(f, fieldnames)
            c.writeheader()
            c.writerows(events)

        self.stdout.write(self.style.SUCCESS("done"))
