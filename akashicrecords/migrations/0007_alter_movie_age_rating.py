# Generated by Django 3.2.13 on 2023-11-13 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akashicrecords', '0006_auto_20231113_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='age_rating',
            field=models.CharField(max_length=10),
        ),
    ]