# Generated by Django 4.0.6 on 2022-11-25 15:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0008_alter_bibfiles_insertdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bibfiles',
            name='insertDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 25, 15, 58, 39, 658365)),
        ),
    ]
