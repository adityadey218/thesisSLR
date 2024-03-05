from django.db import models
from ..models.literatureCl import LiteratureCl
from ..models.recommendetLit import RecommendetLit



class Recomclassification(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    RecommendetLit_id = models.ForeignKey(RecommendetLit, on_delete=models.CASCADE)



