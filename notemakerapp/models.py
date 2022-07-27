import email
from pyexpat import model
from unicodedata import name
from django.db import models
from requests import request

# Create your models here.


class NewUser(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=15)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = (username)

    @property
    def is_anonymous(arg):
        return False

    @property
    def is_authenticated(arg):
        return True


class registeredUser(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField()
