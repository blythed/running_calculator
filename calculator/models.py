from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Athlete(models.Model):
    best100 = models.FloatField(default=0)
    best200 = models.FloatField(default=0)
    best400 = models.FloatField(default=0)
    best800 = models.FloatField(default=0)
    best1500 = models.FloatField(default=0)
    bestMile = models.FloatField(default=0)
    best5k = models.FloatField(default=0)
    best10k = models.FloatField(default=0)
    bestHM = models.FloatField(default=0)
    bestMar = models.FloatField(default=0)
    gender = models.CharField(max_length=6,default='Male') 
