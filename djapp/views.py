from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Shop
from .tasks import task_1, get_parsing_data


def index(request):

    task_1.delay()

    return HttpResponse("Hello world!")


def parser(request):

    get_parsing_data.delay()

    return HttpResponse("Parsing is already finished")


def product_stats(request):
    alifshop_products_count = Product.objects.filter(shop__id=1).aggregate(
        count=Count('id')
    )
    bemarket_products_count = Product.objects.filter(shop__id=2).aggregate(
        count=Count('id')
    )
    media_park_products_count = Product.objects.filter(shop__id=3).aggregate(
        count=Count('id')
    )
    olcha_products_count = Product.objects.filter(shop__id=4).aggregate(
        count=Count('id')
    )
    sello_products_count = Product.objects.filter(shop__id=5).aggregate(
        count=Count('id')
    )
    texnomart_products_count = Product.objects.filter(shop__id=6).aggregate(
        count=Count('id')
    )
    uzummarket_products_count = Product.objects.filter(shop__id=7).aggregate(
        count=Count('id')
    )

    return HttpResponse(
        f"""
alifshop: {alifshop_products_count['count']}<br>
bemarket: {bemarket_products_count['count']}<br>
media_park: {media_park_products_count['count']}<br>
olcha: {olcha_products_count['count']}<br>
sello: {sello_products_count['count']}<br>
texnomart: {texnomart_products_count['count']}<br>
uzummarket: {uzummarket_products_count['count']}<br>
"""
    )

def delete_products(request):
    Product.objects.all().delete()

    return HttpResponse(
        'All products have deleted!'
    )


