from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.handleSignup, name='handleSignup'),
    path('logout', views.handleLogout, name='handleLogout'),
    path('login', views.handleLogin, name='handleLogin'),
    path('conversion', views.convert, name='convert'),
    path('editor', views.editor, name="editor"),
    path('collections', views.collections, name="collections"),
    path('edit', views.edit, name="editor"),
    path('editor', views.editor, name="edit")

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
