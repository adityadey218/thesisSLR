from django.db import models


class LiteratureCl(models.Model):
    issn = models.CharField(max_length=50,  null=True)
    idl = models.CharField(max_length=50,  null=True)
    Abstract = models.CharField(max_length=10000,  null=True)
    Title = models.CharField(max_length=500,  null=True)
    Autherkeywords = models.CharField(max_length=5000,  null=True)
    Indexkeywords = models.CharField(max_length=5000,  null=True)
    Author = models.CharField(max_length=500,  null=True)
    AuthorsID =  models.CharField(max_length=500,  null=True)
    Volume = models.IntegerField(null=True)
    Issue = models.IntegerField(null=True)
    Year = models.IntegerField(null=True)
    Pagestart = models.IntegerField(null=True)
    Pageend= models.IntegerField(null=True)
    Pagecount = models.IntegerField(null=True)
    Source = models.CharField(max_length=400,  null=True)
    ENTRYTYPE = models.CharField(max_length=500,  null=True)
    doi = models.CharField(max_length=5000,  null=True)
    url = models.CharField(max_length=500,  null=True)
    citation_count = models.IntegerField(default=0,  null=True)
    Affiliations = models.CharField(max_length=5000,  null=True)
    Authors_affiliations = models.CharField(max_length=5000,  null=True)
    Address = models.CharField(max_length=5000,  null=True)
    Publisher = models.CharField(max_length=5000,  null=True)
    Language = models.CharField(max_length=500,  null=True)
    AbbreviatedSource = models.CharField(max_length=200,  null=True)
    Document_Type = models.CharField(max_length=500,  null=True)
    Publication_Stage = models.CharField(max_length=100,  null=True)
    Access_Type = models.CharField(max_length=100,  null=True)
    EID = models.CharField(max_length=500,  null=True)
    author_publ_age= models.IntegerField(null=True)
    author_age= models.IntegerField(null=True)
    doc_id= models.IntegerField(null=True)
    author_order= models.IntegerField(null=True)




    def getDoiOnly(self):
        return self.doi.replace("https://doi.org/", "")

    @staticmethod
    def fetchById(id):
        return LiteratureCl.objects.get(id=id)


    def fetchById2(id):
        return LiteratureCl.objects.get(id=id)

