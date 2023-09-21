"""meeting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path, path
from django.contrib import admin
from web import views

urlpatterns = [
    path('',views.main),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^login/', views.login),
    re_path(r'^index/', views.index),
    re_path(r'^booking/', views.booking),
    re_path(r'^personal/', views.personal),
    re_path(r'^bookingpersonal/', views.bookingpersonal),
    re_path(r'^cancelbooking/', views.cancelbooking),

]
