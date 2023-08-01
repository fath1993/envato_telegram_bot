from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from envato.views import RequestFile, envato_auth_view

app_name = 'envato'

urlpatterns = [
    path('request-file&token=<str:token>/', csrf_exempt(RequestFile.as_view()), name='request-file'),
    path('envato-sign-in/', envato_auth_view, name='envato-auth-view'),

    # path('profile-single/', csrf_exempt(ProfileSingle.as_view()), name='profile-single'),
]
