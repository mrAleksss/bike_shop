from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from carts.models import Cart
from orders.models import Order, OrderItem
from .forms import CreateOrderForm


@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user= request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        # Create order
                        order = Order.objects.create(
                            user=user,
                            phone=form.cleaned_data['phone'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        # Create ordered items
                        for cart_item in cart_items:
                            bicycle = cart_item.bicycle
                            name = cart_item.bicycle.name
                            price = cart_item.bicycle.sell_price()
                            quantity = cart_item.quantity

                            if bicycle.quantity < quantity:
                                raise ValidationError(f'Недостатня кількість {name} на складі\
                                                      в наявності - {bicycle.quantity}')
                            
                            OrderItem.objects.create(
                                order=order,
                                bicycle=bicycle,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                            bicycle.quantity -= quantity
                            bicycle.save()

                        # clear user carts after creating order
                        cart_items.delete()

                        messages.success(request, 'Замовлення оформлено')
                        return redirect('user:profile')
            except ValidationError as e:
                messages.warning(request, str(e))
                return redirect('cart:order')
            
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Оформлення замовлення',
        'form': form,
        'order': True,
    }

    return render(request, 'orders/create_order.html', context)
