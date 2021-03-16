import csv

from django.core.management.base import BaseCommand

from geonames_place.models import Place
from radical_translations.utils.models import place_to_dict


class Command(BaseCommand):
    help = "Exports `Place` data into a CSV file."

    def handle(self, *args, **options):
        self.stdout.write("Exporting Places into CSV file places.csv ...", ending=" ")
        places = [
            place_to_dict(place)
            for place in Place.objects.exclude(
                agents=None,
                agents_main_places=None,
                births=None,
                deaths=None,
                event=None,
                resourceplace=None,
            ).select_related("country")
        ]

        if not places:
            self.stderr.write(self.style.NOTICE("No places found!"))
            return -1

        fieldnames = places[0].keys()

        with open("places.csv", "w") as f:
            c = csv.DictWriter(f, fieldnames)
            c.writeheader()
            c.writerows(places)

        self.stdout.write(self.style.SUCCESS("done"))
