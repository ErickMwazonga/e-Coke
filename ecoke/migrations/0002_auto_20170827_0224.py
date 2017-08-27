# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 02:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecoke', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='favourite_drink',
            field=models.CharField(choices=[('CC', 'Coca-Cola'), ('SP', 'Sprite'), ('FT', 'Fanta'), ('CZ', 'Coca-Cola Zero'), ('CL', 'Coca-Cola Life'), ('CT', 'Coca-Cola Light'), ('DS', 'Dasani'), ('MM', 'Minute Maid'), ('Ceil', 'Ceil'), ('PW', 'Powerade'), ('PZ', 'Powerade Zero'), ('SO', 'Simply Orange'), ('FS', 'Fresca'), ('GV', 'Glaceau VitaminWater'), ('GS', 'Glaceau SmartWater'), ('DV', 'Del Valle'), ('MY', 'Mello Yello'), ('FZ', 'Fuze'), ('FA', 'Fuze Tea'), ('HT', 'Honest Tea'), ('OD', 'Odwalla')], max_length=20),
        ),
    ]