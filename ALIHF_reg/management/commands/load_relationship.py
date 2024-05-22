import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from ALIHF_reg.models import *

class Command(BaseCommand):
    help = "Load relationship type data from CSV"

    def handle(self, *args, **options):
        datafile = f"{settings.TEMPLATE_DIR}/helper/relationship.csv"

        with open(datafile) as csvFile:
            reader = csv.reader(csvFile)

            for row in reader:
                RelationshipType.objects.get_or_create(relationship=row[0])

