# Generated by Django 3.2.13 on 2023-12-03 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akashicrecords', '0031_auto_20231203_0413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watched',
            name='rating',
            field=models.FloatField(blank=True, choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')]),
        ),
    ]