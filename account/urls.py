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

from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="account_index"),
    path('login/', views.login, name="account_login"),
    path('logout/', views.logout, name="account_logout"),
    path('register/', views.register, name="account_register"),
    path('profile/', views.profile, name="account_porfile"),
    # path('dashboard/', views._login,name="account_porfile"),

]
