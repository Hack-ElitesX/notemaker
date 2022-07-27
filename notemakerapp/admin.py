from django.contrib import admin
from notemakerapp.models import NewUser, registeredUser

# Register your models here.
admin.site.register(NewUser)
admin.site.register(registeredUser)
