from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.handleSignup,name='handleSignup'),
    path('logout',views.handleLogout,name='handleLogout'),
    path('login',views.handleLogin,name='handleLogin'),
    path('conversion',views.convert,name='convert'),
    path('editor', views.editor, name="editor"),
    path('collections',views.collections, name="collections")
]
