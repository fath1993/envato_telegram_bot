from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from envato.views import RequestFile, envato_auth_view, envato_scraper_start_view

app_name = 'envato'

urlpatterns = [
    path('request-file/', csrf_exempt(RequestFile.as_view()), name='request-file'),
    path('envato-sign-in/', envato_auth_view, name='envato-auth-view'),
    path('envato-start-scraper/', envato_scraper_start_view, name='envato-start-scraper'),
]
