from django.shortcuts import render


def index(request):
    context = {'page_title': 'ربات تلگرامی انواتو قدرت گرفته از پایتون ، جنگو و سلنیوم'}
    return render(request, 'landing.html', context)
