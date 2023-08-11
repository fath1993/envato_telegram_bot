from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from custom_logs.models import CustomLog


@never_cache
def logs_view(request, log_level):
    if log_level == 'debug':
        context = {'page_title': "لاگ عملکرد ربات در سطح برنامه", 'log_level': 'debug'}
    elif log_level == 'info':
        context = {'page_title': "لاگ عملکرد ربات در سطح اطلاعات", 'log_level': 'info'}
    else:
        return JsonResponse({'message': 'Invalid URL'})
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'logs.html', context)
    else:
        return JsonResponse({'message': 'you are not authorized to view the content'})


def ajax_logs_data(request):
    log_level = request.POST['log_level']
    log_list = []
    if log_level == 'debug':
        debug_logs = CustomLog.objects.filter().order_by('-id')[:40]
    else:
        debug_logs = CustomLog.objects.filter(log_level='INFO').order_by('-id')[:40]
    for log in debug_logs:
        log_list.append([log.created_at.strftime('%Y-%m-%d %H:%M'), log.description])
    print(log_list)
    return JsonResponse({'result': log_list})


