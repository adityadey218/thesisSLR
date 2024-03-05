from django.db import models


class RecommendetLit(models.Model):
    Title = models.CharField(max_length=500)
    Link = models.CharField(max_length=500)
    Recomby = models.CharField(max_length=500,  null=True)
    RecomDate= models.CharField(max_length=500, null=True)
    classified = models.CharField(max_length=500,  null=True)
    datePub =  models.CharField(max_length=50,  null=True)
    RecomnB =  models.CharField(max_length=100,  null=True)
    Author1= models.CharField(max_length=50,  null=True)
    doi = models.CharField(max_length=100, null=True)
    second_recommendation = models.CharField(max_length=500,  null=True)
    citation_count = models.IntegerField(null=True)
    affiliation = models.CharField(max_length=100,  null=True)
    affiliation_city = models.CharField(max_length=100,  null=True)
    affiliation_country = models.CharField(max_length=100,  null=True)
    issn = models.CharField(max_length=50)
    idl = models.CharField(max_length=50,  null=True)
    Abstract = models.CharField(max_length=1000,  null=True)
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
    Source = models.CharField(max_length=5000)
    ENTRYTYPE = models.CharField(max_length=500,  null=True)
    doi = models.CharField(max_length=100,  null=True)
    url = models.CharField(max_length=500,  null=True)
    Affiliations = models.CharField(max_length=5000,  null=True)
    Authors_affiliations = models.CharField(max_length=5000,  null=True)
    Address = models.CharField(max_length=500,  null=True)
    Publisher = models.CharField(max_length=500,  null=True)
    Language = models.CharField(max_length=500,  null=True)
    AbbreviatedSource = models.CharField(max_length=50,  null=True)
    Document_Type = models.CharField(max_length=500,  null=True)
    Publication_Stage = models.CharField(max_length=100,  null=True)
    Access_Type = models.CharField(max_length=100,  null=True)
    EID = models.CharField(max_length=500,  null=True)
    Article_type = models.CharField(max_length=100,  null=True)

    def getTitle(self):
        return self.Title

    def getDoiOnly(self):
        return self.doi.replace("https://doi.org/", "")

    @staticmethod
    def fetchById(id):
        return RecommendetLit.objects.get(id=id)


    def fetchById2(id):
        return RecommendetLit.objects.get(id=id)

