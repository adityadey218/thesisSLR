from django import forms
from django.forms import ModelForm
from firstapp.models import KeywordsClass


class Keywordsform(ModelForm):
   # KeyWord = forms.CharField(initial='Add keywords')
   class Meta:
       model = KeywordsClass
       fields = {
           'KeyWord'
       }


