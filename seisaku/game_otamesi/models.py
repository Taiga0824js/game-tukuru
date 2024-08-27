from django.db import models

class Player(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()

class Bullet(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()

class Enemy(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()

# Create your models here.
