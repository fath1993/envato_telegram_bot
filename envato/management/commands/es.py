from django.core.management.base import BaseCommand

from envato.enva_def import get_envato_cookie, check_if_sign_in_is_needed


class Command(BaseCommand):
    def handle(self, *args, **options):
        # get_envato_cookie()
        check_if_sign_in_is_needed()


