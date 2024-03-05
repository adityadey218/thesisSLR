from django.db import models


class KeywordsClass(models.Model):
    KeyWord = models.CharField(max_length=200,)
    objects = models.Manager() # The default manager.