from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

app_name = 'envato-telegram-bot'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('accounts/', include('accounts.urls')),
    path('logs/', include('custom_logs.urls')),
    path('envato/', include('envato.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)