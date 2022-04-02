from django.core.management.base import BaseCommand

from ...parsers.csv_parser import ingredient_parser


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = '../data'
        ingredient_parser(f'{path}/ingredients.csv')
