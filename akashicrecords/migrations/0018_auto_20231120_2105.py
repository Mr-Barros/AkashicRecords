# Generated by Django 3.2.13 on 2023-11-20 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akashicrecords', '0017_auto_20231120_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='box_office',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='imdb_rating',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='imdb_votes',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='metascore',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='runtime',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.IntegerField(blank=True),
        ),
    ]
