from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('parse/', views.parser),
    path('stats/', views.product_stats),
    path('del/', views.delete_products),
]

