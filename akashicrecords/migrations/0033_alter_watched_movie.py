# Generated by Django 3.2.13 on 2023-12-03 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akashicrecords', '0032_alter_watched_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watched',
            name='movie',
            field=models.ManyToManyField(blank=True, null=True, to='akashicrecords.Movie'),
        ),
    ]
