from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from envato.views import RequestFile

app_name = 'envato'

urlpatterns = [
    path('request-file/', csrf_exempt(RequestFile.as_view()), name='request-file'),
    # path('profile-single/', csrf_exempt(ProfileSingle.as_view()), name='profile-single'),
]
