# Generated by Django 3.2.13 on 2023-11-14 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akashicrecords', '0010_profile_watched_movies'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='watched_movies',
        ),
        migrations.AddField(
            model_name='profile',
            name='watched_movies',
            field=models.ManyToManyField(blank=True, to='akashicrecords.Movie'),
        ),
    ]
