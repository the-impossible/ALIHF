import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from ALIHF_reg.models import Countries

class Command(BaseCommand):
    help = "Load country data from CSV"

    def handle(self, *args, **options):
        datafile = f"{settings.TEMPLATE_DIR}/helper/country.csv"

        with open(datafile) as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                Countries.objects.get_or_create(country=row[0])

