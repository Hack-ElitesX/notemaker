from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.login1, name='login1'),
    path('register1/', views.register1, name='register1')

]
