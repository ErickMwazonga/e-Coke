# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from datetime import date

# Create your models here.
class Brand(models.Model):
    '''
    A database representation of a Brand
    '''
    DRINKS =(
        ('CC', 'Coca-Cola'),
        ('SP', 'Sprite'),
        ('FT', 'Fanta'),
        ('CZ', 'Coca-Cola Zero'),
        ('CL', 'Coca-Cola Life'),
        ('CT', 'Coca-Cola Light'),
        ('DS', 'Dasani'),
        ('MM', 'Minute Maid'),
        ('Ceil', 'Ceil'),
        ('PW', 'Powerade'),
        ('PZ', 'Powerade Zero'),
        ('SO', 'Simply Orange'),
        ('FS', 'Fresca'),
        ('GV', 'Glaceau VitaminWater'),
        ('GS', 'Glaceau SmartWater'),
        ('DV', 'Del Valle'),
        ('MY', 'Mello Yello'),
        ('FZ', 'Fuze'),
        ('FA', 'Fuze Tea'),
        ('HT', 'Honest Tea'),
        ('OD', 'Odwalla'),
    )

    collector_name       = models.CharField(max_length=255)
    respondent_name      = models.CharField(max_length=255)
    respondent_city      = models.CharField(max_length=255)
    favourite_drink      = models.CharField(max_length=20, choices=DRINKS)
    date_of_collection   = models.DateField(default=date.today)

    def __str__(self):
        return '%s-%s' % (self.respondent_name, self.favourite_drink)

    class Meta:
        ordering = ['-date_of_collection', 'favourite_drink']