from django.contrib import admin
from . import models



@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'username', 'language', 'is_admin')
    list_editable = ('is_admin',)
    search_fields = ('chat_id',)
    list_filter = ('is_admin',)


@admin.register(models.UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    pass


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
    list_display = ('id', 'title', 'price')
    list_display_links = ('id', 'title')
    list_filter = ('shop',)
    search_fields = ('title', )


@admin.register(models.DataDict)
class DataDictAdmin(admin.ModelAdmin):
    pass




