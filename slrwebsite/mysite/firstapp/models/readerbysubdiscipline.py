from django.db import models
from enum import Enum
from ..models.literatureCl import LiteratureCl
from ..models.mendeley import Mendeley


class Readerbysubdiscipline(models.Model):
    id = models.IntegerField(primary_key=True)
    disname = models.CharField(max_length=100)
    mendely_id = models.ForeignKey(Mendeley, on_delete=models.CASCADE)
    discount = models.IntegerField()
