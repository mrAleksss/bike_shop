from django.urls import path
from goods import views

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog, name='index'),
    path('<slug:product_slug>/', views.product, name='product'),
]