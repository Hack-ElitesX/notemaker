from django.db import models

class Collections(models.Model):
    username = models.CharField(max_length=50,default='User')
    title = models.CharField(max_length=15)
    desc = models.TextField()

    def __str__(self):
        return self.username + str('_') + self.title