# Generated by Django 4.0.6 on 2024-02-01 23:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0028_alter_bibfiles_insertdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bibfiles',
            name='insertDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 1, 23, 16, 15, 516652)),
        ),
    ]