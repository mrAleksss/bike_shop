from django.contrib import admin
from goods.models import Categories, Bicycle


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(Bicycle)
class BicycleAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }
