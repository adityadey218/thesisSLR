from django.db import models
from enum import Enum
from ..models.literatureCl import LiteratureCl
from ..models.altmetrics import Altmetrics


class Authorsaltmetrics(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    altmetrics_id = models.ForeignKey(Altmetrics, on_delete=models.CASCADE)
    citation_all_count = models.IntegerField(blank=True, null=True)




