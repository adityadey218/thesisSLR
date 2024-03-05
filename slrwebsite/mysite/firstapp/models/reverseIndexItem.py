from django.db import models
from enum import Enum
from ..models.literatureCl import LiteratureCl



class ReverseIndexItem(models.Model):
    id = models.IntegerField(primary_key=True)
    literature = models.ForeignKey(LiteratureCl, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    word = models.CharField(max_length=50)
    type = models.CharField(max_length=50)




class WordType(Enum):
    ABSTRACT = 'ABSTRACT',
    KEYWORD = 'KEYWORD',
    TITLE = 'TITLE'




