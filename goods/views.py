from django.shortcuts import render, get_list_or_404
from django.core.paginator import Paginator
from goods.models import Bicycle
from goods.utils import q_search


def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    frame = request.GET.get('frame', None)
    brand = request.GET.get('brand', None)
    wheel_size = request.GET.get('wheel_size', None)
    query = request.GET.get('q', None)

    if category_slug == 'all':
        goods = Bicycle.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = Bicycle.objects.filter(category__slug=category_slug)

    # Querysets for filters
    if on_sale:
        goods = goods.filter(discount__gt=0)
    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)
    if frame:
        goods = goods.filter(frame=frame)
    if brand:
        goods = goods.filter(brand=brand)
    if wheel_size:
        goods = goods.filter(wheel_size=int(wheel_size))

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))

    context = {
        'title': 'Catalog of products',
        'goods': current_page,
        'slug_url': category_slug,
    }
    return render(request, 'goods/catalog.html', context)


def product(request, product_slug):
    product = Bicycle.objects.get(slug=product_slug)
    context = {
        'product': product,
    }

    return render(request, 'goods/product.html', context)
