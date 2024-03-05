from django.db import models
from enum import Enum
from ..models.literatureCl import LiteratureCl



class Authors(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    literature_id = models.ForeignKey(LiteratureCl, on_delete=models.CASCADE)
    lit_date = models.IntegerField(blank=True, null=True)
    citation_all_count = models.IntegerField(blank=True, null=True)
    scopus_author_id = models.IntegerField(blank=True, null=True)

    augender = models.CharField(max_length=10, blank=True, null=True)


    # to be filled from another request (NOT MENDELEY)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    eid = models.IntegerField(blank=True, null=True)
    document_count = models.IntegerField(blank=True, null=True)
    cited_by_count = models.IntegerField(blank=True, null=True)
    citation_count= models.IntegerField(blank=True, null=True)
    name_initials = models.CharField(max_length=50, blank=True, null=True)
    name_indexed =  models.CharField(max_length=50, blank=True, null=True)
    name_surname =  models.CharField(max_length=50, blank=True, null=True)
    name_given =  models.CharField(max_length=50, blank=True, null=True)