from curses import meta
from django.shortcuts import render, redirect
from carts.models import Cart
from goods.models import Bicycle


def cart_add(request, product_slug):
    bicycle = Bicycle.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, bicycle=bicycle)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
        
            Cart.objects.create(user=request.user, bicycle=bicycle, quantity=1)

    return redirect(request.META['HTTP_REFERER'])


def cart_update(request, product_slug):
    ...


def cart_remove(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    
    return redirect(request.META['HTTP_REFERER'])
