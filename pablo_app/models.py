from django.db import models


# Create your models here.
class ContentImage(models.Model):
    file = models.FileField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    style = models.CharField(max_length=511)


class Artist(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    years = models.CharField(max_length=50)
    genre = models.CharField(max_length=400)
    nationality = models.CharField(max_length=255)
    bio = models.CharField(max_length=2000)
    wikipedia = models.CharField(max_length=300)


class Painting(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    path = models.CharField(max_length=511)