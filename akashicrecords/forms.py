from django.forms import ModelForm
from .models import Movie
from django import forms

class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieSearchForm(forms.Form):
  q = forms.CharField(label='Search for a movie', max_length=100)
