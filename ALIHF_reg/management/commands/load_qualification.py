import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from ALIHF_reg.models import *

class Command(BaseCommand):
    help = "Load qualification data from CSV"

    def handle(self, *args, **options):
        datafile = f"{settings.TEMPLATE_DIR}/helper/qualification.csv"

        with open(datafile) as csvFile:
            reader = csv.reader(csvFile)

            for row in reader:
                Qualifications.objects.get_or_create(qualification=row[0])