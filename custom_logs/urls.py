from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from custom_logs.views import logs_view, ajax_logs_data

app_name = 'logs'
urlpatterns = [
    path('<str:log_level>/', logs_view, name='logs'),
    path('ajax-logs-data', ajax_logs_data, name='ajax-logs-data'),
]

