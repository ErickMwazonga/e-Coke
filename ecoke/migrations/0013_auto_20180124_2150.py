# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-24 21:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecoke', '0012_auto_20180123_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='date_of_collection',
            field=models.DateField(default=datetime.date(2018, 1, 24)),
        ),
    ]
