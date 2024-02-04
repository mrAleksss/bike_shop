from django.contrib import admin
from orders.models import Order, OrderItem

# admin.site.register(Order)
# admin.site.register(OrderItem)

class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem
    fields = ('bicycle', 'name', 'price', 'quantity')
    search_fields = ('bicycle', 'name')
    extra = 0


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = 'order', 'bicycle', 'name', 'price', 'quantity'
    search_fields = ('order', 'bicycle', 'name')


class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = ('requires_delivery', 'status', 'payment_on_get', 'is_paid', 'created_at')
    search_fields = ('requires_delivery', 'payment_on_get', 'is_paid', 'created_at')
    readonly_fields = ('created_at',)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'requires_delivery', 'status', 'payment_on_get', 'is_paid', 'created_at']
    search_fields = ['id']
    readonly_fields = ('created_at',)
    list_filter = ['requires_delivery', 'status', 'payment_on_get', 'is_paid']
    inlines = (OrderItemTabulareAdmin,)