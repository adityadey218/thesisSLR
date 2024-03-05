from django.db import models
from enum import Enum
from ..models.literatureCl import LiteratureCl
from ..models.mendeley import Mendeley


class Readerbysubarea(models.Model):
    id = models.IntegerField(primary_key=True)
    subname = models.CharField(max_length=100)
    mendely_id = models.ForeignKey(Mendeley, on_delete=models.CASCADE)
    subcount = models.IntegerField()
