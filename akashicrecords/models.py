from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
  title = models.CharField(max_length = 300)
  year = models.IntegerField(null=True)
  end_year = models.IntegerField(null=True)
  rated = models.CharField(max_length = 10)
  released = models.CharField(max_length = 20)
  runtime = models.IntegerField(null=True)
  genre = models.CharField(max_length = 100)
  director = models.CharField(max_length = 200)
  writer = models.CharField(max_length = 200)
  actors = models.CharField(max_length = 1000)
  plot = models.CharField(max_length = 10000)
  language = models.CharField(max_length = 100)
  country = models.CharField(max_length = 100)
  awards = models.CharField(max_length = 300)
  poster = models.CharField(max_length = 1000)
  metascore = models.IntegerField(null=True)
  imdb_rating = models.FloatField(null=True)
  imdb_votes = models.IntegerField(null=True)
  imdb_id = models.CharField(max_length = 10)
  type = models.CharField(max_length = 10)
  dvd = models.CharField(max_length = 50, blank=True)
  box_office = models.IntegerField(null=True)
  production = models.CharField(max_length = 50, blank=True)
  website = models.CharField(max_length = 200, blank=True)
  total_seasons = models.CharField(max_length = 50, blank=True)


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField(max_length=500, blank=True)
  image = models.ImageField(default='default.png', upload_to='profile_images')
  watched_movies = models.ManyToManyField(Movie)

  def __str__(self):
    return self.user.username


class Watched(models.Model):
  RATING = [
    (0, '0'), 
    (0.5, '0.5'),
    (1, '1'),
    (1.5, '1.5'),
    (2, '2'),
    (2.5, '2.5'),
    (3, '3'),
    (3.5, '3.5'),
    (4, '4'),
    (4.5, '4.5'),
    (5, '5'),
  ]
  
  user = models.ManyToManyField(User)
  date = models.DateTimeField(auto_now_add=True)
  rating = models.FloatField(choices=RATING)

class Comment(models.Model):
  user_comment = models.ManyToManyField(User)
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
  comment = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)