import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Uploads .csv to Ingredient model'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding='utf-8') as f:
            reader = csv.reader(f, dialect='excel')
            for row in reader:
                _, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )
