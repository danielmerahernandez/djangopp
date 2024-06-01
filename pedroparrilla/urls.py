"""
URL configuration for pedroparrilla project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from montos.views import *
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('montos/',include(('montos.urls','montos'))),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('inicio/', login_required(index), name='index'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)), 

]
