from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Назва')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорію'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name


class Bicycle(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Назва')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Опис')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Картинка')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Ціна')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Знижка в %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Кількість')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категорія')
    wheel_size = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Розмір коліс')
    frame = models.CharField(max_length=100, default='steel', verbose_name='Матеріал рами')
    frame_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='Розмір рами')
    brand = models.CharField(max_length=100, verbose_name='Бренд')
    series = models.CharField(max_length=100, verbose_name='Серія')

    class Meta:
        db_table = 'product'
        verbose_name = 'Велосипед'
        verbose_name_plural = 'Велосипеди'
        ordering = ('id',)

    def __str__(self):
        return f'{self.brand} | {self.series}'

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'product_slug': self.slug})
    
    def display_id(self):
        return f'{self.id:05}'
    
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price*self.discount/100, 2)
        return self.price
