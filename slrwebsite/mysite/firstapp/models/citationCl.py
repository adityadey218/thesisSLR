from django.db import models
from ..models.literatureCl import LiteratureCl


class CitationCl(models.Model):
    id = models.IntegerField(primary_key=True)
    citation_count = models.IntegerField(blank=True, null=True)
    Literature_id = models.ForeignKey(LiteratureCl, on_delete=models.CASCADE)

