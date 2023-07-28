import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'envato_telegram_bot.c_settings.prod')

application = get_wsgi_application()
