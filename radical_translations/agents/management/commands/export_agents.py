import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from radical_translations.agents.models import Organisation, Person


class Command(BaseCommand):
    help = "Exports `Agent` data into a CSV file."

    def handle(self, *args, **options):
        self.to_csv(Organisation, "organisations")
        self.to_csv(Person, "persons")

    def to_csv(self, cls, title):
        self.stdout.write(
            f"Exporting {title.title()} into CSV files {title}.csv ...",
            ending=" ",
        )
        agents = [agent.to_dict() for agent in cls.objects.all()]

        if not agents:
            self.stderr.write(self.style.NOTICE(f"No {title} found!"))
            return

        fieldnames = agents[0].keys()

        with open(os.path.join(settings.EXPORTS_ROOT, f"{title}.csv"), "w") as f:
            c = csv.DictWriter(f, fieldnames)
            c.writeheader()
            c.writerows(agents)

        self.stdout.write(self.style.SUCCESS("done"))
