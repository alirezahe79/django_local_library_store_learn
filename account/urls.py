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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="account_index"),
    path('login/', views.login, name="account_login"),
    path('logout/', views.logout, name="account_logout"),
    path('register/', views.register, name="account_register"),
    path('profile/', views.profile, name="account_porfile"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="account/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_comeplete/', auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_done.html"), name="password_reset_complete"),
    # path('dashboard/', views._login,name="account_porfile"),

]
