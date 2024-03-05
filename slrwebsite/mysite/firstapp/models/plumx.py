from django.db import models
from datetime import datetime
from ..models.literatureCl import LiteratureCl
from ..models.recommendetLit import RecommendetLit



class Plumx(models.Model):

    Literature_id = models.ForeignKey(LiteratureCl, on_delete=models.CASCADE)
    #recLiterature_id = models.ForeignKey(RecommendetLit, on_delete=models.CASCADE)
    Citation_count = models.IntegerField(blank=True, null=True)
    Citation_det = models.CharField(max_length=500, blank=True, null=True)
    cited_by_count = models.IntegerField(blank=True, null=True)
    cited_by_count_sources=models.CharField(max_length=500, blank=True, null=True)
    Scopus_cit_count = models.IntegerField(blank=True, null=True)
    Crossref = models.IntegerField(blank=True, null=True)
    SSRN = models.IntegerField(blank=True, null=True)
    PubMedCentralEurope = models.IntegerField(blank=True, null=True)
    SciELO = models.IntegerField(blank=True, null=True)
    Aci_cit = models.IntegerField(blank=True, null=True)
    pubmed=models.IntegerField(blank=True, null=True)
    patentfam_count = models.IntegerField(blank=True, null=True)
    patentfam_count_sources = models.CharField(max_length=500, blank=True, null=True)
    Patent_families = models.IntegerField(blank=True, null=True)
    Clinical_citedby_count=models.IntegerField(blank=True, null=True)
    NICE = models.IntegerField(blank=True, null=True)
    PubMed_Guidelines_cot=models.IntegerField(blank=True, null=True)
    DynaMed_Plus = models.IntegerField(blank=True, null=True)
    Clinical_citedby_count_sources=models.CharField(max_length=500, blank=True, null=True)
    policy_count =models.IntegerField(blank=True, null=True)
    Policy_citation = models.IntegerField(blank=True, null=True)

    Social_count = models.IntegerField(blank=True, null=True)
    Social_det = models.CharField(max_length=500, blank=True, null=True)
    Tweet_count = models.IntegerField(blank=True, null=True)
    FB_count = models.IntegerField(blank=True, null=True)

    Mention_count = models.IntegerField(blank=True, null=True)
    Mention_det = models.CharField(max_length=500, blank=True, null=True)
    News_count = models.IntegerField(blank=True, null=True)
    Blog_count = models.IntegerField(blank=True, null=True)
    reference_count=models.IntegerField(blank=True, null=True)
    QA_site_mentioncount =models.IntegerField(blank=True, null=True)
    link_count =models.IntegerField(blank=True, null=True)
    Comment_count= models.IntegerField(blank=True, null=True)

    Capture_count = models.IntegerField(blank=True, null=True)
    Capture_det = models.CharField(max_length=500, blank=True, null=True)
    Reader_count = models.IntegerField(blank=True, null=True)
    export_save = models.IntegerField(blank=True, null=True)
    download_ct = models.IntegerField(blank=True, null=True)
    Book_mark_count = models.IntegerField(blank=True, null=True)


    Usage_count = models.IntegerField(blank=True, null=True)
    Usage_det = models.CharField(max_length=500, blank=True, null=True)
    abstract_view=models.IntegerField(blank=True, null=True)
    link_click_count=models.IntegerField(blank=True, null=True)
    link_out=models.IntegerField(blank=True, null=True)
    Fulltxt_viw=models.IntegerField(blank=True, null=True)

    @staticmethod
    def fetchById(id):
        return Plumx.objects.get(id=id)