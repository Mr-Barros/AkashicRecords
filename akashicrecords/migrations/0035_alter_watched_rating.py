# Generated by Django 3.2.13 on 2023-12-03 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akashicrecords', '0034_auto_20231203_0422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watched',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
