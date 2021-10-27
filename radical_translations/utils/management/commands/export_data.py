import os
from shutil import make_archive

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Exports all the data into a CSV files and compress them into a single file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--compress",
            action="store_true",
            default=False,
            help="Don't export the data, compresses existing export.",
        )

    def handle(self, *args, **options):
        if not options["compress"]:
            call_command("export_agents")
            call_command("export_events")
            call_command("export_places")
            call_command("export_resources")

        self.stdout.write("Compressing exported files ...", ending=" ")
        make_archive(
            os.path.join(settings.MEDIA_ROOT, "data"),
            "zip",
            settings.EXPORTS_ROOT,
        )
        self.stdout.write(self.style.SUCCESS("done"))
