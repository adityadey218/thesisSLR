from django.db import models
from datetime import datetime
from ..models.literatureCl import LiteratureCl
from ..models.recommendetLit import RecommendetLit



class Altmetrics(models.Model):

    Literature_id = models.ForeignKey(LiteratureCl, on_delete=models.CASCADE)
    #recLiterature_id = models.ForeignKey(RecommendetLit, on_delete=models.CASCADE)
    altmetric_jid = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=500, blank=True, null=True)
    altmetric_id = models.IntegerField(blank=True, null=True)
    journal=models.CharField(max_length=500, blank=True, null=True)
    is_oa = models.BooleanField(blank=True, null=True)
    schema = models.CharField(max_length=50, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    cited_by_posts_count = models.IntegerField(blank=True, null=True)
    cited_by_msm_count= models.IntegerField(blank=True, null=True)
    cited_by_policies_count= models.IntegerField(blank=True, null=True)
    cited_by_tweeters_count= models.IntegerField(blank=True, null=True)
    cited_by_fbwalls_count= models.IntegerField(blank=True, null=True)
    cited_by_rh_count= models.IntegerField(blank=True, null=True)
    cited_by_patents_count= models.IntegerField(blank=True, null=True)
    cited_by_accounts_count= models.IntegerField(blank=True, null=True)
    last_updated= models.IntegerField(blank=True, null=True)
    added_on =  models.IntegerField(blank=True, null=True)
    published_on =  models.IntegerField(blank=True, null=True)

    readers_count =  models.IntegerField(blank=True, null=True)
    citeulike_reader = models.IntegerField(blank=True, null=True)
    mendeley = models.IntegerField(blank=True, null=True)
    connotea = models.IntegerField(blank=True, null=True)



