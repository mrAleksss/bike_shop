from django.urls import path
from carts import views

app_name = 'carts'

urlpatterns = [
    path('cart_add/<slug:product_slug>/', views.cart_add, name='cart_add'),
    path('cart_update/<slug:product_slug>/', views.cart_update, name='cart_update'),
    path('cart_remove/<slug:product_slug>/', views.cart_remove, name='cart_remove'),
]