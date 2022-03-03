"""alirezastore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name="cart_home"),
    path('add/<int:id_pro>', views.add_cart, name="add_cart"),
    path('add_api', views.add_api_cart, name="add_api_cart"),
    path('delete_cart_num', views.delete_cart_num, name="delete_cart_num"),
    path('delete_cart', views.delete_cart, name="delete_cart"),
]
