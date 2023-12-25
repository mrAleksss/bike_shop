from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {
        'title': 'Home Page',
        'content': 'Головна сторінка нашого сайту'
    }
    return render(request, 'main/index.html', context)


def about(request):
    return HttpResponse('<h1>About us</h1>')
