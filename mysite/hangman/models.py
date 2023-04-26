from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Scoreboard(models.Model):

    def __str__(self):
        return self.username

    username = models.CharField(max_length=1000, null=True, default="test")
    word = models.CharField(max_length=1000, null=True)
    wordSize = models.IntegerField(max_length=50, null=True)
    score = models.IntegerField(max_length=1, null=True)