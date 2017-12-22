# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)

    activation_key = models.CharField(max_length=255, default=1)
    email_validated = models.BooleanField(default=False)

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    def __str__(self):
        return self.user.username


class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.name + "-" + self.email


# Create your models here.
class Brand(models.Model):
    '''
    A database representation of a Brand
    '''
    DRINKS = (
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

    collector_name = models.CharField(max_length=255)
    respondent_name = models.CharField(max_length=255)
    respondent_city = models.CharField(max_length=255)
    favourite_drink = models.CharField(max_length=20, choices=DRINKS)
    date_of_collection = models.DateField(default=timezone.now().date())

    def __str__(self):
        return '%s-%s' % (self.respondent_name, self.favourite_drink)

    class Meta:
        ordering = ['-date_of_collection', 'favourite_drink']
        unique_together = ('collector_name', 'respondent_name')
