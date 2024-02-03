from django.contrib import admin
from goods.models import Categories, Bicycle


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',),}
    list_display = ('name',)


@admin.register(Bicycle)
class BicycleAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name',),}
    list_display = ['name', 'quantity', 'price', 'discount']
    list_editable = ['discount', 'quantity']
    search_fields = ['name', 'description']
    list_filter = ['discount', 'quantity', 'category']
    fields = [
              'name', 
              ('brand', 'series'), 
              'category', 'slug', 
              'description', 
              'image', 
              ('price', 'discount'), 
              'quantity', 
              'wheel_size', 
              'frame', 
              'frame_size']
