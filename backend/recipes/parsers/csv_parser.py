import csv

from ..models import Ingredient, Unit


def ingredient_parser(file):
    with open(file) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            unit_pk, created = Unit.objects.get_or_create(name=row[1])
            Ingredient.objects.create(name=row[0], measurement_unit=unit_pk)
