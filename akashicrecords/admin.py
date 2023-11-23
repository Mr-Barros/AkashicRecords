from django.contrib import admin
from .models import Movie, Profile, Watched, Comment

# Register your models here.
admin.site.register(Movie)
admin.site.register(Profile)
admin.site.register(Watched)
admin.site.register(Comment)