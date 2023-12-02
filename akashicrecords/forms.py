from django.contrib.auth.models import User
from .models import Movie, Profile, Watched
from django import forms

# class MovieForm(ModelForm):
#     class Meta:
#         model = Movie
#         fields = '__all__'


class MovieSearchForm(forms.Form):
  q = forms.CharField(label='Search for a movie', max_length=100)

class UserUpdateForm(forms.ModelForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['bio' ,'image']

class AddWatched(forms.ModelForm):
  class Meta:
    model = Watched
    fields=['user', 'rating', 'movie']

# class Recommendation(forms.ModelForm):
  