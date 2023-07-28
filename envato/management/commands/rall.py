from django.core.management.base import BaseCommand
from custom_logs.models import CustomLog


def clear_data():
    pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        clear_data()
