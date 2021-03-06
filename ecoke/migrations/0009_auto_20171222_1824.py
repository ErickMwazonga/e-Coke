# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-22 18:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecoke', '0008_auto_20171220_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='date_of_collection',
            field=models.DateField(default=datetime.date(2017, 12, 22)),
        ),
        migrations.AlterUniqueTogether(
            name='brand',
            unique_together=set([('collector_name', 'respondent_name')]),
        ),
    ]
