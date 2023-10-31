from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField(max_length=500, blank=True)
  image = models.ImageField(default='default.png', upload_to='profile_images')

  def __str__(self):
    return self.user.username

  
  

class Movie(models.Model):
  AGE_RATING = [
    ('G', 'G'),
    ('PG', 'PG'),
    ('PG_13', 'PG_13'),
    ('R', 'R'),
    ('NC_17', 'NC_17'),
  ]
  
  title = models.CharField(max_length = 300)
  director = models.CharField(max_length = 300)
  release_date = models.DateField()
  age_rating = models.CharField(max_length = 5, choices = AGE_RATING)
  runtime = models.CharField(max_length = 300)
  genre = models.CharField(max_length = 300)
  main_cast = models.CharField(max_length = 1000)
  rating = models.CharField(max_length = 300)
  # imdb_rating = models.CharField(max_length = 300)
  # rotten_tomatoes_rating = models.CharField(max_length = 300)
  plot = models.CharField(max_length = 10000)
  poster = models.ImageField(upload_to = 'images/')
  box_office = models.CharField(max_length = 300)