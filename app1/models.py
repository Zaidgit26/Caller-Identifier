from django.db import models

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password1 = models.CharField(max_length=100)
    def __str__(self):
        return self.username
