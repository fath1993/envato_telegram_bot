from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from accounts.views import SignUp

app_name = 'accounts'

urlpatterns = [
    path('signup/', csrf_exempt(SignUp.as_view()), name='signup'),
    # path('profile-single/', csrf_exempt(ProfileSingle.as_view()), name='profile-single'),
]
