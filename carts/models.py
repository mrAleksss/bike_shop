from django.db import models
from goods.models import Bicycle
from users.models import User


class CartQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    user = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Юзер')
    bicycle = models.ForeignKey(to=Bicycle, on_delete=models.CASCADE, verbose_name='Велосипед')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Кількість')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Час додавання')

    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзину'
        verbose_name_plural = 'Корзини'

    objects = CartQueryset().as_manager()

    def products_price(self):
        return round(self.bicycle.sell_price() * self.quantity, 2)

    def __str__(self):
        return f'Корзина: {self.user.username} | {self.bicycle.name} | {self.quantity} шт.'