# Generated by Django 4.0.6 on 2023-01-10 21:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0012_alter_bibfiles_insertdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bibfiles',
            name='insertDate',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 10, 21, 33, 34, 861362)),
        ),
    ]