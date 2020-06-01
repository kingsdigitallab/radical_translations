import json
from urllib import request

from django.core.management.base import BaseCommand

from radical_translations.core.models import Resource
from radical_translations.utils.models import get_gsx_entry_value


class Command(BaseCommand):
    help = (
        "Imports `Resource`.`electronic_locator` data from a data collection "
        "spredsheet."
    )

    def add_arguments(self, parser):
        parser.add_argument("url", nargs=1, type=str, help="The URL to the JSON file.")

    def handle(self, *args, **options):
        url = options["url"][0]

        with request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            entries = data["feed"]["entry"]

            self.stdout.write("Importing URLs...")
            for entry in entries:
                main_title = get_gsx_entry_value(entry, "title")
                if not main_title:
                    continue

                url = get_gsx_entry_value(entry, "url")
                if not url:
                    continue

                date_display = get_gsx_entry_value(entry, "year")

                try:
                    if date_display:
                        resource = Resource.objects.get(
                            _is_paratext=False,
                            title__main_title=main_title,
                            date__date_display=date_display,
                        )
                    else:
                        resource = Resource.objects.get(
                            _is_paratext=False, title__main_title=main_title
                        )
                except (Resource.DoesNotExist, Resource.MultipleObjectsReturned):
                    self.stdout.write(
                        self.style.ERROR(f"- Error getting resource: {main_title}")
                    )
                    continue

                resource.electronic_locator = url
                resource.save()
