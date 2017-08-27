# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 12:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collector_name', models.CharField(max_length=255)),
                ('respondent_name', models.CharField(max_length=255)),
                ('respondent_city', models.CharField(max_length=255)),
                ('favourite_drink', models.CharField(choices=[('Coca-Cola', 'Coca-Cola'), ('Sprite', 'Sprite'), ('Fanta', 'Fanta'), ('Coca-Cola Zero', 'Coca-Cola Zero'), ('Coca-Cola Life', 'Coca-Cola Life'), ('Coca-Cola Light', 'Coca-Cola Light'), ('Dasani', 'Dasani'), ('Minute Maid', 'Minute Maid'), ('Ceil', 'Ceil'), ('Powerade', 'Powerade'), ('Powerade Zero', 'Powerade Zero'), ('Simply Orange', 'Simply Orange'), ('Fresca', 'Fresca'), ('Glaceau VitaminWater', 'Glaceau VitaminWater'), ('Glaceau SmartWater', 'Glaceau SmartWater'), ('Del Valle', 'Del Valle'), ('Mello Yello', 'Mello Yello'), ('Fuze', 'Fuze'), ('Fuze Tea', 'Fuze Tea'), ('Honest Tea', 'Honest Tea'), ('Odwalla', 'Odwalla')], max_length=20)),
                ('date_of_collection', models.DateField(default=datetime.date.today)),
            ],
            options={
                'ordering': ['-date_of_collection'],
            },
        ),
    ]
