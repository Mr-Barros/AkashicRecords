# Generated by Django 3.2.13 on 2023-11-20 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akashicrecords', '0012_alter_profile_watched_movies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='dvd',
            field=models.CharField(max_length=100),
        ),
    ]
