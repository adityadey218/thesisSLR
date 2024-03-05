from django.db import models
from datetime import datetime



class BibFiles(models.Model):
    id = models.IntegerField(primary_key=True)
    fileName = models.CharField(max_length=500)
    isProcessed = models.BooleanField(default=False)
    insertDate = models.DateTimeField(default=datetime.now())

    @staticmethod
    def getAllUnProcessedFiles():
        queryset = BibFiles.objects.filter(isProcessed=False)
        return queryset

