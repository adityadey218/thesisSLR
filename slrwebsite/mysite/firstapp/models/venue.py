from django.db import models
from datetime import datetime

class Venue(models.Model):
    journal = models.CharField(max_length=150)
    cst = models.FloatField()
    cstyear = models.IntegerField()
    csc = models.FloatField()
    cscyear = models.IntegerField()
    sjr = models.FloatField()
    sjryear = models.IntegerField()
    snip = models.FloatField()
    snipyear = models.IntegerField()


    @staticmethod
    def fetchById(id):
        return Venue.objects.get(id=id)