from django.contrib import admin

# Register your models here.
from .models import Product, Category, Carousel


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
    'name', 'image', 'description', 'price', 'category', 'stock', 'sales', 'is_on', 'recommend', 'create_time')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_time')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'create_time')
    list_filter = ('title',)
    search_fields = ('title',)
