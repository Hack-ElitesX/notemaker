from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login', views.login1, name='login1'),
    path('conversion/', views.conversion, name='conversion'),
    path('register1/', views.register1, name='register1')

]
