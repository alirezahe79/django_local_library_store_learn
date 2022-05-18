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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name="products_home"),
    path('admin/', views.index2, name="products_home_admin"),
    path('delete/<int:id_cat>', views.delete, name="delete_product"),
    path('add/', views.add, name="add_product"),
    path('delete_pro/', views.delete_pro, name="delete_pro"),
    path('edit/<int:id_pro>', views.edit, name="edit_product"),
    path('get/subcategories', views.get_subcategories, name="get_subcategories"),
    path('base/', views.test, name="base"),
    path('<str:namemain>/<int:page>', views.TabProducts, name="tabviewname"),
    path('<str:namemain>/', views.index_cat, name="product_cat"),
    path('<int:page>', views.TabProducts2, name="tabviewname2"),
    path('number_sep2022', views.number_seprator, name="number_seprator"),
    path('<str:subname>/<int:id_pro>', views.product_details, name="product_details"),
]
