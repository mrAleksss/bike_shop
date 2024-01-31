from django.urls import path
from carts import views

app_name = 'carts'

urlpatterns = [
    path('cart_add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart_update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('cart_remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]