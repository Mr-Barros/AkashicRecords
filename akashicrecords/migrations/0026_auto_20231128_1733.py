# Generated by Django 3.2.13 on 2023-11-28 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akashicrecords', '0025_watched_movie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='user_comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='profile',
            field=models.ManyToManyField(blank=True, to='akashicrecords.Profile'),
        ),
    ]
