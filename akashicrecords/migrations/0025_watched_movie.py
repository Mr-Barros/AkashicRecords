# Generated by Django 3.2.13 on 2023-11-28 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akashicrecords', '0024_auto_20231121_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='watched',
            name='movie',
            field=models.ManyToManyField(to='akashicrecords.Movie'),
        ),
    ]
