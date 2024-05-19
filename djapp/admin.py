from django.contrib import admin
from . import models


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    list_filter = ('shop',)
