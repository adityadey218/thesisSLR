# Generated by Django 4.0.6 on 2023-07-30 15:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0020_alter_bibfiles_insertdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bibfiles',
            name='insertDate',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 30, 15, 52, 49, 541555)),
        ),
    ]