# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 02:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecoke', '0002_auto_20170827_0224'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'ordering': ['-date_of_collection', 'favourite_drink']},
        ),
    ]