from cgitb import text
from django.db import models

class Collection(models.Model):
    username = models.CharField(max_length=50,default='User')
    title = models.CharField(max_length=15)
    desc = models.TextField()
    text = models.TextField(max_length=150, default="")

    def __str__(self):
        return self.username + str('_') + self.title