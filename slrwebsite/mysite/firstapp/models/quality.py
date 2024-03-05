from django.db import models
from ..models.literatureCl import LiteratureCl



class Quality(models.Model):
    id = models.IntegerField(primary_key=True)
    literature_id = models.ForeignKey(LiteratureCl, on_delete=models.CASCADE)
    Citation_count = models.IntegerField(blank=True, null=True)


    Lit_title = models.CharField(max_length=500, blank=True, null=True)

    page = models.IntegerField(blank=True, null=True)
    authors_all_count = models.FloatField(blank=True, null=True)
    publication_type= models.FloatField(blank=True, null=True)
    publisher = models.FloatField(blank=True, null=True)
    abstract_structured = models.FloatField(blank=True, null=True)
    cst = models.FloatField(blank=True, null=True)
    csc = models.FloatField(blank=True, null=True)
    sjr = models.FloatField(blank=True, null=True)
    snip = models.FloatField(blank=True, null=True)
    Citation_count = models.FloatField(blank=True, null=True)
    Social_count = models.FloatField(blank=True, null=True)
    Mention_count = models.FloatField(blank=True, null=True)
    Capture_count = models.FloatField(blank=True, null=True)
    Usage_count = models.FloatField(blank=True, null=True)
    KW_hit_in_kw = models.FloatField(blank=True, null=True)
    KW_hit_in_title= models.FloatField(blank=True, null=True)
    KW_hit_in_abstract= models.FloatField(blank=True, null=True)
    KW_hit_in_all = models.FloatField(blank=True, null=True)



    @staticmethod
    def fetchById(id):
        return Quality.objects.get(id=id)





