# Generated by Django 4.0.6 on 2022-11-14 14:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='altmetrics',
            name='is_oa',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bibfiles',
            name='insertDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 14, 14, 50, 36, 80638)),
        ),
    ]
