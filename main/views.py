from django.shortcuts import render
from django.http import HttpResponse
from goods.models import Categories


def index(request):
    categories = Categories.objects.all()

    context = {
        'categories': categories,
        'title': 'Магазин Velos',
        'content': 'Магазин Velos пропонує вам широкий вибір велосипедів на будь-який смак'
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'Про Нас',
        'content': 'Про нашу Кампанію',
        'text_on_page': 'Текст чому саме наш магазин такий класний і хороший',
    }
    return render(request, 'main/about.html', context)
