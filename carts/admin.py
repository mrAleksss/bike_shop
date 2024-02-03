from django.contrib import admin
from carts.models import Cart


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = 'bicycle', 'quantity', 'created_at'
    search_fields = 'bicycle', 'quantity', 'created_at'
    readonly_fields = ('created_at',)
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'bicycle_display', 'quantity', 'created_at']
    list_filter = ['created_at', 'user', 'bicycle__name']

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return 'Анонімний юзер'
    
    def bicycle_display(self, obj):
        return str(obj.bicycle.name)

