
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template.response import TemplateResponse
from bs4 import BeautifulSoup
import urllib
import urllib.request
import json
import scipy
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg

from django.http import HttpResponse
from matplotlib import pylab
from pylab import *
import chartjs

from django.db import connection
from bibtexparser.bparser import BibTexParser
from scipy.stats import pearsonr
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import time
from .models import KeywordsClass, LiteratureCl, BibFiles, WordType, Quality
from .processor import BibFileProcessor, SearchManager, ScienceDirect
from urllib.request import urlopen

from . forms import Keywordsform


from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
import csv


def index(request):
   if request.method == 'POST':
        form = Keywordsform(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('index'))

   else:
          form = Keywordsform()
   context = {"myKwForm" :form}
   return render(request,'firstapp/index.html',context=context)



def listkw(request):
    if request.method == 'GET':
        b = BibFileProcessor()
        s = ScienceDirect()
        #steps to gather all info related to recommendet publ

        #1 get the dois
        #b.getRecomLitdoi()

        #2 get some meta data
        #b.getRecomLitInfo()

        #get plumx
        #b.plumxsave()
        #b.plumxsaveforRec()
        #b.plumxsaveElsv()

        #b.citationrecomLiterature()
        #get altmetrics
        #b.altmetricssaveforRec()

        #get mendely
        #b.getMendeleyfulldata()


        # for authors paper
        #b.splitauthorsforICSE()
        b.getauthorsdata_byscopusid()
        b.plumxsaveElsv()


        #get author gender
        #b.getauthorGender()

        #get author order
        #b.getauthornumber()
        #b.getpagescount()

        # try get authors with not already filled data
        #b.getauthorsdata_byscopusidFtilter()
        #b.getgender()

        # get author gender
        #b.getauthorGender()

        #get missing dois from IEEE
        #b.getLitdoiIeee()

       #ICSE
        #get doi for ICSE papers
        #b.getpaperdoi()
        #get the authors id from the old data
        #b.getauthorsidfromtable()
        # get authors id from same title
        #b.getauthorsidfromsame_title()
        #get author ids from same author name
        #b.getauthorsidfrom_authersname()
        #b.getauthorsidfrom_authersname()
        #b.getauthorsidfromsame_title()
        #b.fillauthosmissingIds()
        #b.fillauthosmissingIds_bytitle()
        #b.fillauthosmissingIds_DOIISNULL()
        #SearchManager.myselect()
        #b.fillauthosmissingIds_bydois()
        #b.getauthorIDsfromNAMES()

        #b.splitauthorsforICSE()
        #b.citationrecomLiterature()
        #s.getPlumxdata()
        #b.getLitInfo()
        #b.getLitcitationNew()
        #b.getLitcitationNew_bytitle()
        #b.plumxsave()
        #b.plumxsave()
        #b.citationLiterature()
        #b.sourcesave()
        #b.qualitysave()

        #author age paper
        #b.get_co_author_Reputation()
        #b.get_co_author_Reputation()
        #b.get_co_author_Reputation_MT_only()
        #b.get_authorall_authors_paperscount()
        #b.get_authorall_authors_MTpaperscount()
        #b.get_paper_Reputation_MT_only_all_conf()
        datakw = KeywordsClass.objects.all()
    return render(request, 'firstapp/index.html')


def startProcess(request):
    if request.method == 'POST':
        response_data = {}
        # get Plumx data
        try:
            b = BibFileProcessor()

            #get dois
            #b.getLitInfo()
           # b.plumxsave()

            # source data try
           # b.sourcesave()

            # update literature table adding citation count
            #b.citationLiterature()

            # Last step save the quality table
            #b.qualitysave()


        except:
            response_data['result'] = 'error'
            response_data['message'] = 'Exception has occured'
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        # print(b.venueCSTmaxTotal())

        response_data['result'] = 'success'
        response_data['message'] = 'Data loaded successfully! You will be redirected automatically to search page'
        return HttpResponse(json.dumps(response_data), content_type="application/json")


# Imaginary function to handle an uploaded file.
def handle_uploaded_file(f, fileName):
    with open((fileName), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# This is the first page
def bibpage(request):
    if request.method == 'GET':
        return render(request, 'firstapp/bibpage.html')
    #if request.method == 'POST':
    #    file = request.FILES['file_import']
    #    fileName = file.name
    #    handle_uploaded_file(file, fileName)
    #    newBibFile = BibFiles()
    #    newBibFile.fileName = fileName
    #    newBibFile.save()
    #    b = BibFileProcessor()
    #    b.saveBibFileInTable()
    #    return render(request, 'firstapp/listkw.html')
    #  if request.method == 'GET':
    #      b = BibFileProcessor()
          # b.saveExcInTable()
          # for recommendation data
          # b.saveRecommndsExcInTable()
          #b.saveAuthpubExcInTable()
    #      b.savecoviddocsExcInTable()
     #     b.saveBibFileInTable()
          #b.saveYusraToolcsvInTable()
     #    return render(request, 'firstapp/listkw.html')

    if request.method == 'POST':
        b = BibFileProcessor()
         # b.saveAuthpubExcInTable()
        b.savecoviddocsExcInTable()
        b.altmetricssaveforRec()
     #     b.saveBibFileInTable()
         # b.saveYusraToolcsvInTable()
        return render(request, 'firstapp/listkw.html')



# This page is not used as it is only for searching keywords not (Boolean operation related)
def contentsearch(request):
    # normal search
    if request.method == 'GET':
       kwsearchRs =[]
       keywordsl = ['virtual,reality', 'data']
       for item in SearchManager.searchByKeywordsLogicalOperation(keywordsl):
           kwsearchRs.append(item)
    return TemplateResponse(request, 'firstapp/contentsearch.html', {"datakw" : keywordsl, "kwsearchRs": kwsearchRs})


# this is the main search page for content analysis
def search(request):
    if request.method == 'POST':
        isAllFieldsFound = False
        counter = 1
        keywords = []
        while (not isAllFieldsFound):
            fieldName = "text_keyword_" + str(counter)
            if fieldName in request.POST:
                newWord = request.POST.get(fieldName)
                if len(newWord) > 0:
                    k = KeywordsClass()
                    k.KeyWord = newWord
                    k.save()
                    keywords.append(newWord)
            else: 
                isAllFieldsFound = True
            counter += 1
        kwsearchRs =[]
        datakw = KeywordsClass.objects.all()
        #keywordsl = ['virtual,reality', 'data']
        groupByKeywords = {}
        groupCounts = {}
        group = 1
        keywordsByGroup = {}
        print("Keyword:",keywords)
        for keyword in keywords:
            list = keyword.split(',')
            for word in list:
                groupByKeywords[word.strip()] = group
                if str(group) not in keywordsByGroup:
                    keywordsByGroup[str(group)] = keyword
            group = group + 1
        result = SearchManager.searchByKeywordsLogicalOperation(keywords)
        print("Result:",result)
        for item in result:
            currentWordGroup = groupByKeywords[item[0]]
            if not (item[2] in groupCounts):
                groupCounts[item[2]] = {currentWordGroup: item[1]}
            elif not (currentWordGroup in groupCounts[item[2]]):
                groupCounts[item[2]][currentWordGroup] = item[1]
            else:
                groupCounts[item[2]][currentWordGroup] += item[1]
        
        documentsFindCount = {}
        for documentId in groupCounts:
            groupCounter = groupCounts[documentId]
            total_count = 0
            for groupId in groupCounter:
                if not documentId in documentsFindCount:
                    documentsFindCount[documentId] = 0
                count = groupCounter[groupId]
                newItem = (keywordsByGroup[str(groupId)], count, documentId)
                documentsFindCount[documentId] = documentsFindCount[documentId] + count
                kwsearchRs.append(newItem)

                #save the count hits in quality table by updating it
                total_count = total_count + count

        print(documentsFindCount.values())

        maxHitsFromDocuments = max(documentsFindCount.values())
        for documentId in documentsFindCount:
            documentsFindCount[documentId] = documentsFindCount[documentId] / (maxHitsFromDocuments * 1.0)
            quality = Quality.objects.get(literature_id=documentId)
            quality.KW_hit_in_all = round(documentsFindCount[documentId],4)
            quality.save()

        return TemplateResponse(request, 'firstapp/search.html', {"datakw" : datakw, "kwsearchRs": kwsearchRs})
    return TemplateResponse(request, 'firstapp/search.html', {"datakw" : [], "kwsearchRs": {}})


def searchByAuthor(request):

    htmlFileUrl = "firstapp/searchByAuthor.html"
    count = 0
    if request.method == 'GET':
        print("Get in SearchByAuthor")
    #search keywords match in abstract, keywords, title
    if request.method == 'POST':
        firstName = request.POST.get('txtAuthorFirstName')
        lastName = request.POST.get('txtAuthorLastName')
        if lastName and firstName:
            scienceDirect = ScienceDirect()
            count = scienceDirect.getDocumentCountByAuthor(firstName, lastName)
        else:
            return TemplateResponse(request, htmlFileUrl, {"error" : "Please, fill all required filed"})

    return TemplateResponse(request, htmlFileUrl, {"count" : count, "kwsearchRs": ""})

# display the quality scoring table
def quality_scoring(request):

    # normal search
    if request.method == 'GET':
       litList =[]
       x = [1, 2, 3, 4, 5]
       b = BibFileProcessor()
       for item in b.getQulaity():
           litList.append(item)

    return TemplateResponse(request, 'firstapp/quality_scoring.html', {"litList": litList})


# Charts pages
class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]

# Charts pages
def tryonly(request):

    line_chart = TemplateView.as_view(template_name='tryonly.html')
    line_chart_json = LineChartJSONView.as_view()

    return TemplateResponse(request, 'firstapp/tryonly.html')

# Charts pages
def chart(request):
    #pearson corr
    chartData = SearchManager.getcorrelationcolumns_panda()


    return TemplateResponse(request, 'firstapp/chart.html', {"chart_data": chartData})

def amona(request):
    #pearson corr
    #chartData = SearchManager.getcorrelationcolumns_panda()


    return TemplateResponse(request, 'firstapp/amona.html')

# Charts pages
def chartspearman(request):

    # spearman
    chartData = SearchManager.getspearmancor_panda()

    return TemplateResponse(request, 'firstapp/chartspearman.html', {"chart_data": chartData})


