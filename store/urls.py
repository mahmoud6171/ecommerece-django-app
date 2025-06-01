from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='store'),
    path('product/<slug:slug>/', views.product_info, name='product_info'),
    path('search/<slug:slug>/', views.list_category, name='list_category'),
]

