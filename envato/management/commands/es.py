from django.core.management.base import BaseCommand
from envato.tasks import envato_scraper


class Command(BaseCommand):
    def handle(self, *args, **options):
        envato_scraper()


