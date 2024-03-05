from ..models.bibFiles import  BibFiles
from ..models.literatureCl import LiteratureCl
from ..models.recommendetLit import RecommendetLit
from ..models.recomclassification import Recomclassification
from ..models.reverseIndexItem import ReverseIndexItem, WordType
from ..models.authors import Authors
from ..models.sourceDate import SourceData
from ..models.venue import Venue
from ..models.plumx import Plumx
from ..models.authorsmendely import Authorsmendely
from ..models.quality import Quality
from bibtexparser.bparser import BibTexParser
from gender_predictor.GenderClassifier import classify_gender




from nltk import FreqDist
import nltk

from string import punctuation
from nltk.corpus import stopwords
from .scienceDirect import ScienceDirect
from bs4 import BeautifulSoup
import urllib
import urllib.request
import csv
import json



class BibFileProcessor:
    max_total_authors = -1
    max_citation_count= -1
    max_usage_count = -1
    max_capture_count = -1
    max_mention_count = -1
    max_sm_count = -1
    max_twitter_count = -1
    max_sjr_count = -1
    max_snip_count =-1
    max_csc_count =-1
    max_cst_count =-1

    @staticmethod
    def plumxusagemaxTotal():
        plumx_all_list = Plumx.objects.all()
        total_usage_per_lit = 0
        total_max_count = 0
        for liplum in plumx_all_list:
            if liplum.Usage_count is None:
                liplum.Usage_count = 0
            liplum.save()

        plumx_all_list2 = Plumx.objects.all()
        for liplum2 in plumx_all_list2:
            if liplum2.Usage_count > total_usage_per_lit:
                total_usage_per_lit = liplum2.Usage_count
        BibFileProcessor.max_usage_count = total_usage_per_lit
        return total_usage_per_lit

    @staticmethod
    def plumxcapturemaxTotal():
        plumx_all_list = Plumx.objects.all()
        total_capture_per_lit = 0
        total_max_count = 0
        for liplum in plumx_all_list:
            if liplum.Capture_count is None:
                liplum.Capture_count = 0
            liplum.save()

        plumx_all_list2 = Plumx.objects.all()
        for liplum2 in plumx_all_list2:
            if liplum2.Capture_count > total_capture_per_lit:
                total_capture_per_lit = liplum2.Capture_count
        BibFileProcessor.max_capture_count = total_capture_per_lit
        return total_capture_per_lit

    @staticmethod
    def plumxmentionmaxTotal():
        plumx_all_list = Plumx.objects.all()
        total_mention_per_lit = 0
        for liplum in plumx_all_list:
            if liplum.Mention_count is None:
                liplum.Mention_count = 0
            liplum.save()

        plumx_all_list2 = Plumx.objects.all()
        for liplum2 in plumx_all_list2:
            if liplum2.Mention_count > total_mention_per_lit:
                total_mention_per_lit = liplum2.Mention_count
        BibFileProcessor.max_mention_count = total_mention_per_lit
        return total_mention_per_lit

    @staticmethod
    def plumxsocialmaxTotal():
        plumx_all_list = Plumx.objects.all()
        total_sm_per_lit = 0
        for liplum in plumx_all_list:
            if liplum.Social_count is None:
                liplum.Social_count = 0
            liplum.save()

        plumx_all_list2 = Plumx.objects.all()
        for liplum2 in plumx_all_list2:
            if liplum2.Social_count > total_sm_per_lit:
                total_sm_per_lit = liplum2.Social_count
        BibFileProcessor.max_sm_count = total_sm_per_lit
        return total_sm_per_lit

    @staticmethod
    def plumxtwittermaxTotal():
        plumx_all_list = Plumx.objects.all()
        total_tw_per_lit = 0
        for liplum in plumx_all_list:
            if liplum.Social_det is None:
                liplum.Social_det = 0
            liplum.save()

        plumx_all_list2 = Plumx.objects.all()
        for liplum2 in plumx_all_list2:
            i = int(liplum2.Social_det)
            if i > total_tw_per_lit:
                total_tw_per_lit = i
        BibFileProcessor.max_twitter_count = total_tw_per_lit
        return total_tw_per_lit

    @staticmethod
    def venueSJRmaxTotal():
        venue_all_list = Venue.objects.all()
        total_sjr_per_lit = 0
        for liplum2 in venue_all_list:
            if liplum2.sjr > total_sjr_per_lit:
                total_sjr_per_lit = liplum2.sjr
        BibFileProcessor.max_sjr_count = total_sjr_per_lit
        return total_sjr_per_lit

    @staticmethod
    def venueSNIPmaxTotal():
        venue_all_list = Venue.objects.all()
        total_snip_per_lit = 0
        for liplum2 in venue_all_list:
            if liplum2.snip > total_snip_per_lit:
                total_snip_per_lit = liplum2.snip
        BibFileProcessor.max_snip_count = total_snip_per_lit
        return total_snip_per_lit

    @staticmethod
    def venueCSCmaxTotal():
        venue_all_list = Venue.objects.all()
        total_csc_per_lit = 0
        for liplum2 in venue_all_list:
            if liplum2.csc > total_csc_per_lit:
                total_csc_per_lit = liplum2.csc
        BibFileProcessor.max_csc_count = total_csc_per_lit
        return total_csc_per_lit


    @staticmethod
    def venueCSTmaxTotal():
        venue_all_list = Venue.objects.all()
        total_cst_per_lit = 0
        for liplum2 in venue_all_list:
            if liplum2.cst > total_cst_per_lit:
                total_cst_per_lit = liplum2.cst
        BibFileProcessor.max_cst_count = total_cst_per_lit
        return total_cst_per_lit


    @staticmethod
    def authorsmaxTotal():
        Literature_all_list = LiteratureCl.objects.all()
        total_count_per_auther = 0
        total_max_count=0
        for li in Literature_all_list:
            literatur_authers = Authors.objects.filter(literature_id=li)
            total_count_per_auther=0
            for li_au in literatur_authers:
                total_count_per_auther= total_count_per_auther + li_au.citation_all_count
            if total_count_per_auther > total_max_count:
                total_max_count = total_count_per_auther
                total_count_per_auther=0

        BibFileProcessor.max_total_authors =total_max_count
        return total_max_count

    @staticmethod
    def citationmaxTotal():
        Literature_all_list = LiteratureCl.objects.all()
        total_count_per_lit = 0
        total_max_count = 0
        for li in Literature_all_list:
            if  li.citation_count > total_count_per_lit:
                total_count_per_lit = li.citation_count
        BibFileProcessor.max_citation_count = total_count_per_lit
        return total_count_per_lit



    @staticmethod
    def authorsTotal(literature):
        literatur_authers = Authors.objects.filter(literature_id=literature)
        total_count=0
        for li in literatur_authers:
            total_count = total_count + li.citation_all_count
        return total_count

    @staticmethod
    def plumx_lit(literature):
        literatur_plumx = Plumx.objects.filter(Literature_id_id=literature)

        return literatur_plumx

    # get citation count and update the literarture table
    def citationLiterature(self):
        scienceDirect = ScienceDirect()
       # Literature_all_list = LiteratureCl.objects.all()
        Literature_all_list = LiteratureCl.objects.filter(id__lte=10736, id__gte=10733)
        for lit in Literature_all_list:
            print(lit.id)
            if lit.doi is "":
                lit.citation_count = 0
            else:
                lit.citation_count = scienceDirect.getCitationCount2(lit)
            lit.save()
        return

    # get all info for the recommended literture from scopus api and update the RecommendetLit table
    def getLitInfo(self):
        scienceDirect = ScienceDirect()
        RecommendetLit_list = LiteratureCl.objects.all()
        for Rlit in RecommendetLit_list:
            print(Rlit.Title)
            Rlit.doi = scienceDirect.getLitInfo(Rlit)
            #Rlit.save()
        return

    def getLitcitationNew(self):
        scienceDirect = ScienceDirect()
        RecommendetLit_list = LiteratureCl.objects.all()
        for lit in RecommendetLit_list:
            print(lit.id)
            if lit.doi is "":
                lit.citation_count = 0
            if lit.doi is None:
                lit.citation_count = 0
            else:
                lit.citation_count = scienceDirect.getLitcitNew(lit.doi)
                lit.save()
        return

    def getLitcitationNew_bytitle(self):
        scienceDirect = ScienceDirect()
        RecommendetLit_list = LiteratureCl.objects.all()
        i=0
        for lit in RecommendetLit_list:
            print(lit.Title)
            if lit.citation_count is None:
                lit.citation_count = scienceDirect.getLitcitNewusingtitel(lit.Title)
                lit.save()

        return


# TO WRITE ABT THIS
    #http://bib-it.sourceforge.net/help/fieldsAndEntryTypes.php#proceedings
    @staticmethod
    def publicationType(literature):

        returnvalue =0
        pubtype = literature.ENTRYTYPE
        if pubtype in ["article", "proceedings", "inproceedings", "book", "incollection"]:
            returnvalue = 1
        else:
            returnvalue=0
        return returnvalue

    @staticmethod
    def publisher(literature):
        returnvalue = 0
        pubtype = literature.ENTRYTYPE
        if pubtype in ["article", "book", "incollection","inbook"]:
            returnvalue = 1
        elif pubtype in ["inproceedings", "manual", "proceedings","techreport"]:
            returnvalue =0.5
        else :
            returnvalue = 0

        return returnvalue

    @staticmethod
    def pagesnumber(literature):

        returnvalue = 0
        vol = literature.volume
        if vol > 6:
            returnvalue = 1
        if vol >= 4 and vol <= 6:
            returnvalue = 0.5
        if vol <4:
            returnvalue = 0

        return returnvalue

    @staticmethod
    def structuredabstract(literature):
        if literature is None:
            return 0
        foundWordsCount = 0
        # search if all of them are in the abstract give 1 if 3 of them give 0.5 if none give 0
        keywordsl = ['introduction', 'objectives', 'methods', 'results','conclusion']
        abstract = literature.abstract.lower()
        if abstract is not None:
            for k in keywordsl:
                if k in abstract:
                    foundWordsCount = foundWordsCount + 1
        if foundWordsCount == 5:
            return 1
        elif foundWordsCount >= 3:
            return 0.5
        return  0


# call this procedure then the search for keywords, because the search will update the exsiting quality record for the lit
    def qualitysave(self):
       BibFileProcessor.citationmaxTotal()
       BibFileProcessor.authorsmaxTotal()
       BibFileProcessor.plumxusagemaxTotal()
       BibFileProcessor.plumxcapturemaxTotal()
       BibFileProcessor.plumxmentionmaxTotal()
       BibFileProcessor.plumxsocialmaxTotal()
       BibFileProcessor.plumxtwittermaxTotal()
       BibFileProcessor.venueCSCmaxTotal()
       BibFileProcessor.venueCSTmaxTotal()
       BibFileProcessor.venueSJRmaxTotal()
       BibFileProcessor.venueSNIPmaxTotal()

       Literature_all_list = LiteratureCl.objects.all()
       i=0
       for lit in Literature_all_list:
           quality = Quality()
           quality.journal = lit.journal
           quality.literature_id = lit
           quality.Lit_title= lit.title
           quality.page = BibFileProcessor.pagesnumber(lit)

           quality.authors_all_count = round(BibFileProcessor.authorsTotal(lit)/BibFileProcessor.max_total_authors,4)
           quality.Citation_count = round(lit.citation_count/BibFileProcessor.max_citation_count,4)

           #Venue Journal data
           try:
               venue = Venue.objects.get(journal=lit.journal)
               #venue = Venue.objects.filter(journal=lit.journal).first()
               quality.snip = round(venue.snip/BibFileProcessor.max_snip_count,4)
               quality.sjr = round(venue.sjr/BibFileProcessor.max_sjr_count,4)
               quality.csc = round(venue.csc/BibFileProcessor.max_csc_count,4)
               quality.cst = round(venue.cst/BibFileProcessor.max_cst_count,4)
           except Venue.DoesNotExist:
               venue = None


           #PLumX
           try:
              plumx = Plumx.objects.get(Literature_id=lit)
              if plumx.Capture_count is None:
                  quality.Capture_count =0
              else:
                  quality.Capture_count = round(plumx.Capture_count/BibFileProcessor.max_capture_count,4)
              if plumx.Social_count is None:
                  quality.Social_count =0
              else:
                  quality.Social_count= round(plumx.Social_count/BibFileProcessor.max_sm_count,4)
              if plumx.Usage_count is None:
                  quality.Usage_count=0
              else:
                 quality.Usage_count = round(plumx.Usage_count/BibFileProcessor.max_usage_count,4)
              if plumx.Mention_count is None:
                  quality.Mention_count =0
              else:
                  quality.Mention_count = round(plumx.Mention_count/BibFileProcessor.max_mention_count,4)

              # we save twitter in KW_hit_in_kw field
              if plumx.Social_det is None:
                  quality.KW_hit_in_kw =0
              else:
                  quality.KW_hit_in_kw = round(int(plumx.Social_det)/BibFileProcessor.max_twitter_count,4)

           except Plumx.DoesNotExist:
                  plumx = None

           quality.publication_type = BibFileProcessor.publicationType(lit)
           quality.publisher = BibFileProcessor.publisher(lit)

           quality.abstract_structured = BibFileProcessor.structuredabstract(lit)

           quality.save()
       return


    def sourcesave(self):
       scienceDirect = ScienceDirect()
       Literature_all_list = LiteratureCl.objects.all()
       for lit in Literature_all_list:
          if not Venue.objects.filter(journal=lit.Source).exists():
               datakw1 = scienceDirect.getSourcedataScopus(lit.Source)
               if datakw1 is not None:
                   if len(datakw1) != 0:
                       i = 0
                       venue = Venue()
                       venue.journal = lit.Source
                       venue.snip = float(datakw1[0].SNIPList[i]['value'])
                       venue.snipyear = int(datakw1[0].SNIPList[i]['year'])
                       venue.sjr= float(datakw1[0].SJRList[i]['value'])
                       venue.sjryear = int(datakw1[0].SJRList[i]['year'])
                       venue.csc = float(datakw1[0].citeScoreCurrentMetric['value'])
                       venue.cscyear = int(datakw1[0].citeScoreCurrentMetric['year'])
                       venue.cst = float(datakw1[0].citeScoreTracker['value'])
                       venue.cstyear = int(datakw1[0].citeScoreTracker['year'])
                       venue.save()
                       i = i+1
       return

    def plumxsaveBsoup(self):
       Literature_all_list = LiteratureCl.objects.all()
       i=0
       for lit in Literature_all_list:
           url = "https://plu.mx/plum/a/?doi={}".format(lit.getDoiOnly())
           print(url)
           r = urllib.request.urlopen(url)
           soup = BeautifulSoup(r, "html.parser")
           plumx = Plumx()
           plumx.Literature_id=lit
           g_data_usage = soup.select("div.metric-counts-container ul.move-right li.metric-counts-citation div.u-h2")
           for i in g_data_usage:
               print(g_data_usage)
               plumx.Usage_count = int(i.text)
           g_data_capture = soup.select("div.metrics-data dl.metrics-capture span.metric-total")
           for i in g_data_capture:
               plumx.Capture_count = int(i.text)
           g_data_sm = soup.select("div.metrics-data dl.metrics-socialMedia span.metric-total")
           for i in g_data_sm:
               plumx.Social_count = int(i.text)
           g_data_citation = soup.select("div.metrics-data dl.metrics-citation span.metric-total")
           for i in g_data_citation:
               plumx.Citation_count = int(i.text)
           g_data_ment = soup.select("div.metrics-data dl.metrics-mention span.metric-total")
           for i in g_data_ment:
               plumx.Mention_count = int(i.text)
           plumx.save()
       return


    def plumxsave(self):
       scienceDirect = ScienceDirect()
       Literature_all_list = LiteratureCl.objects.all()
       #Literature_all_list = LiteratureCl.objects.filter(id__lte=9772, id__gte=5595)

       for lit in Literature_all_list:
           print(lit.id)
           scienceDirect.getPlumxdata(lit)
       return

    def plumxsaveElsv(self):
        scienceDirect = ScienceDirect()
        Literature_all_list = LiteratureCl.objects.all()
        for lit in Literature_all_list:
            if lit.doi is "" or lit.doi is None:
               print("no doi")
               scienceDirect.getPlumxdataElsv(lit.EID,lit)
        return

    @staticmethod
    def splitAuthers(auther_str,literature,year_of_lit):
        scienceDirect = ScienceDirect()
        authers_list = auther_str.split(' and ')
        for a in authers_list:
                author_m = Authors()
                author_m.name = a
                print(a)
                author_m.literature_id = literature
                author_m.lit_date = year_of_lit
                author_m.citation_all_count = scienceDirect.getDocumentCountByAuthorFullname(a)
                author_m.save()
        return

    @staticmethod

    def makeTokens(atext,textype,literaturebelong):
        thelist = ["the"]

        stopWords = stopwords.words('english') + list(punctuation) + thelist
        tokenslist = nltk.word_tokenize(atext)
        fdist = FreqDist(tokenslist)
        wordsFiltered = []
        tokenslist2 = [word for word in tokenslist if not word.isnumeric()]
        tokenslist3 = [word for word in tokenslist2 if len(word) > 1]
        tokenslist4 = [word for word in tokenslist3 if not (word in stopWords)]


        fdist = FreqDist(tokenslist4)

        for w in tokenslist4:
            if w not in stopWords:
               if w not in  wordsFiltered:
                reverseidxite = ReverseIndexItem()
                reverseidxite.word = w.lower()
                reverseidxite.count = fdist[w]
                reverseidxite.literature = literaturebelong
                reverseidxite.type = textype
                reverseidxite.save()
                wordsFiltered.append(w.lower())
        return


    def saveBibFileInTable(self):
        filesToProcess = BibFiles.getAllUnProcessedFiles()
        scienceDirect = ScienceDirect()
        for f in filesToProcess:
            fullFilePath =  f.fileName
            file = open(fullFilePath)
            file.seek(0)
            datakw = file.read()
            bp = BibTexParser(interpolate_strings=False)
            bib_database = bp.parse(datakw)
            for entry in bib_database.entries:
                literature = LiteratureCl()
                if 'title' in entry:
                    literature.title = entry['title']
                literature.idl = entry['ID']
                if 'issn' in entry:
                    literature.issn = entry['issn']
                else:
                    literature.issn = "None"
                if 'volume' in entry:
                    literature.volume = entry['volume']
                    #literature.volume = 0
                else:
                    literature.volume =0
                literature.year = entry['year']
                if 'journal' in entry:
                    literature.journal = entry['journal']
                else:
                    literature.journal = "None"
                literature.ENTRYTYPE = entry['ENTRYTYPE']
                if 'abstract' in entry:
                    literature.abstract = entry['abstract']
                if 'keywords' in entry:
                    literature.keywords = entry['keywords']
                if 'url' in entry:
                    literature.url = entry['url']
                if 'doi' in entry:
                    literature.doi = entry['doi']
                if 'author' in entry:
                    literature.author = entry['author']

                literature.save(force_insert=True)
                print(literature.id)

                #self.makeTokens(literature.title, WordType.TITLE.name, literature)
                #if 'abstract' in entry:
                #   self.makeTokens(literature.abstract, WordType.ABSTRACT.name, literature)
                #if 'keywords' in entry:
                #   self.makeTokens(literature.keywords, WordType.KEYWORD.name, literature)
                #if 'author' in entry:
                #  self.splitAuthers(literature.author, literature, literature.year)
            f.isProcessed = True
            f.save()
        return

    #Retrieve all quality data from the data_base

    def getQulaity(self):
        quality_all_list = Quality.objects.all()
        for quality in quality_all_list:
            if quality.KW_hit_in_all is None:
                quality.KW_hit_in_all = 0
            if quality.cst is None:
                quality.cst = 0
            if quality.csc is None:
                quality.csc = 0
            if quality.sjr is None:
                quality.sjr=0
            if quality.snip is None:
                quality.snip = 0
            if quality.Social_count is None:
               quality.Social_count=0
            if quality.Mention_count is None:
               quality.Mention_count=0
            if quality.Capture_count is None:
               quality.Capture_count=0
            if quality.Usage_count is None:
               quality.Usage_count=0
            if  quality.Citation_count is None:
                quality.Citation_count = 0
            if quality.authors_all_count is None:
                quality.authors_all_count=0
            if quality.KW_hit_in_kw is None:
                quality.KW_hit_in_kw = 0
            quality.save()


        quality_all_list2 = Quality.objects.all()
        for quality2 in quality_all_list2:
            # all the quality criteria
            temp  = quality2.KW_hit_in_all + quality2.page + quality2.abstract_structured + quality2.Citation_count + quality2.cst + quality2.csc + quality2.sjr + quality2.snip + quality2.authors_all_count  + quality2.publisher + quality2.Social_count + quality2.Mention_count + quality2.Capture_count + quality2.Usage_count

            quality2.KW_hit_in_abstract = round(temp,4)
            quality2.save()
        quality_all_list2 = Quality.objects.all().order_by('-KW_hit_in_abstract')
        allLitList = []
        for lit in quality_all_list2:
            allLitList.append(lit)
        return allLitList

    def saveExcInTable(self):
        with open('Files/scopus1.csv', newline='', encoding = "ISO-8859-1") as csvfile:
            csv_data = csv.reader(csvfile, delimiter=',')
            line_count = 0
            for row in csv_data:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count = line_count + 1

                else:
                    line_count = line_count + 1
                    lCi = LiteratureCl()
                    lCi.Author = row[0]
                    lCi.AuthorsID = row[1]
                    lCi.Title = row[2]
                    lCi.Year = row[3]
                    lCi.Source = row[4]
                    lCi.Volume = row[5]
                    if row[6] != '':
                        lCi.Issue = row[6]
                    if row[8] != '':
                        lCi.Pagestart = row[8]
                    if row[9] != '':
                        lCi.Pageend = row[9]
                    if row[10] != '':
                        lCi.Pagecount = row[10]
                    if row[11] != '':
                        lCi.citation_count = row[11]
                    lCi.doi = row[12]
                    lCi.url = row[13]
                    lCi.Affiliations = row[14]
                    lCi.Authors_affiliations = row[15]
                    lCi.Abstract = row[16]
                    lCi.Autherkeywords = row[17]
                    lCi.Indexkeywords = row[18]
                    lCi.Publisher = row[21]
                    lCi.issn = row[22]
                    lCi.Document_Type = row[28]
                    lCi.Publication_Stage = row[29]
                    lCi.Access_Type = row[30]
                    lCi.EID = row[32]


                    lCi.save(force_insert=True)
        return



    @staticmethod
    #this method splits the list of classifications for a recommendet literature
    def splitClassifications(classifications_str,recliterature):
        classification_list = classifications_str.split('-')
        for a in classification_list:
                recomclassification = Recomclassification()
                recomclassification.name = a
                recomclassification.RecommendetLit_id = recliterature
                recomclassification.save()
        return

    @staticmethod
    def splitAuthers2(authers_list,literature, autherid_str):
       if autherid_str != "0":
            #authers_list = authers_list.split(',')
            if "," not in autherid_str:
                autherid_str = autherid_str
            if "," in autherid_str:
               autherid_list = autherid_str.split(',')
            elif ";" in autherid_str:
                autherid_list = autherid_str.split(';')
            for auth_id in autherid_list:
                if auth_id !="":
                    author_m = Authors()
                    author_m.name = authers_list
                    author_m.scopus_author_id =auth_id
                    author_m.literature_id = literature
                    author_m.save()
            return

    def getpagescount(self):
        #LiteratureCl_all_list = LiteratureCl.objects.all()
        LiteratureCl_all_list = LiteratureCl.objects.filter(id__lte=34454, id__gte=20513)

        for lit in LiteratureCl_all_list:
            pagescount = lit.ENTRYTYPE
            if pagescount != "":
                   if "-" in pagescount:
                       pages_list = pagescount.split('-')
                       if len(pages_list) == 2:
                           if pages_list[1] =="":
                               lit.Pagecount = 1
                               lit.save()
                           else:
                               nbofpages = int(pages_list[1]) - int(pages_list[0])+1
                               lit.Pagecount = nbofpages
                               lit.save()

                   elif "-" not in pagescount:
                       lit.Pagecount = 1
                       lit.save()

        return




    @staticmethod
    def splitAuthers3(authers_list, literature, autherid_str):
           if autherid_str != "":
               if ";" in autherid_str:
                   autherid_list = autherid_str.split(';')
                   for auth_id in autherid_list:
                       if auth_id != "":
                           author_m = Authors()
                           author_m.name = authers_list
                           author_m.scopus_author_id = auth_id
                           author_m.literature_id = literature
                           author_m.save()
               elif ";" not in autherid_str:
                   author_m = Authors()
                   author_m.name = authers_list
                   author_m.scopus_author_id = autherid_str
                   author_m.literature_id = literature
                   author_m.save()

               return

    def splitauthorsforICSE(self):
        #Literature_all_list = LiteratureCl.objects.all()
        Literature_all_list = LiteratureCl.objects.filter(id__lte=9444, id__gte=4400)
        for lit in Literature_all_list:
            self.splitAuthers3(lit.Author,lit,lit.AuthorsID)
        return


    def saveRecommndsExcInTable(self):
        with open('Files/run_results_diss_csv.csv', newline='', encoding = "ISO-8859-1") as csvfile:
            csv_data = csv.reader(csvfile, delimiter=',')
            line_count = 0
            for row in csv_data:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count = line_count + 1

                else:
                    line_count = line_count + 1
                    lCi = RecommendetLit()
                    lCi.Title = row[0]
                    lCi.Link = row[1]
                    lCi.Recomby = row[2]
                    lCi.RecomnB = row[3]
                    lCi.datePub =row[4]
                    lCi.classified = row[5]
                    lCi.Author1 = row[6]
                    lCi.second_recommendation =row[7]
                    lCi.save(force_insert=True)
                    self.splitClassifications(row[5],lCi)

        return

    def saveAuthpubExcInTable(self):
        with open('Files/allconf.csv', newline='', encoding = "ISO-8859-1") as csvfile:
            csv_data = csv.reader(csvfile, delimiter=',')
            line_count = 0
            for row in csv_data:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count = line_count + 1

                else:
                    line_count = line_count + 1
                    lCi = LiteratureCl()
                    # author_order
                    if row[0] != '':
                       lCi.author_order = row[0]
                        #author_url
                    if row[1] != '':
                       lCi.AuthorsID = row[1]
                        #authors
                    if row[2] != '':
                        lCi.Authors_affiliations = row[2]
                    #collection
                    if row[3] != '':
                       lCi.Source = row[3]
                     #current_author
                    if row[4] != '':
                       lCi.Author = row[4]
                      #doi
                    if row[5] != '':
                       lCi.doi = row[5]
                    #authorf_year
                    if row[6] != '':
                       lCi.Pagestart = row[6]
                    #authorl_yaer
                    if row[7] != '':
                       lCi.Pageend = row[7]
                     #paginatin
                    if row[8] != '':
                       lCi.ENTRYTYPE = row[8]
                        #title
                    if row[9] != '':
                        lCi.Title = row[9]
                     #year
                    if row[10] != '':
                        lCi.Year = row[10]
                    # conf
                    if row[11] != '':
                        lCi.AbbreviatedSource = row[11]
                    # Maintrack
                    if row[12] != '':
                        lCi.Issue = row[12]
                    #author_age
                    if row[13] != '':
                       lCi.author_age = row[13]
                    #author_publ_age
                    if row[14] != '':
                       lCi.author_publ_age = row[14]
                    #pagenumber
                    if row[15] != '':
                       lCi.Pagecount = row[15]
                    lCi.save(force_insert=True)

        return

# this is the final authors data function from scopus
    def getauthorsdata_byscopusid(self):
        scienceDirect = ScienceDirect()
        #auth_all_list = Authors.objects.all()
        auth_all_list = Authors.objects.filter(id__lte=29043, id__gte=28229)

        for auth in auth_all_list:
            print(auth.id)
            #scienceDirect.fillauthosdata_scopus(auth)
            scienceDirect.fillauthosdata_scopustoken(auth)

        return


# in this fuction we check if the authors data already inserted, if so we dont request this info again
    # there should be another function where we add the data for the new record from old already exsiting one
    def getauthorsdata_byscopusidFtilter(self):
        full_author_id_list =[]
        scienceDirect = ScienceDirect()
        # auth_all_list = Authors.objects.all()
        auth_all_list_full = Authors.objects.filter(id__lte=18000, id__gte=1)
        auth_all_list_empty = Authors.objects.filter(id__lte=19551, id__gte=18001)

        # start_year__isnull=True

        for auth_full in auth_all_list_full:
            full_author_id_list.append(auth_full.scopus_author_id)

        full_author_id_list = list(dict.fromkeys(full_author_id_list))
        for auth in auth_all_list_empty:
              if auth.scopus_author_id not in full_author_id_list:
                print(auth.scopus_author_id)
                scienceDirect.fillauthosdata_scopus(auth)
                #scienceDirect.fillauthosdata_scopustoken(auth)
                #else get it from the db

        return


    def getRecomLitdoi(self):
        scienceDirect = ScienceDirect()
        RecLiterature_all_list = RecommendetLit.objects.all()
        for lit in RecLiterature_all_list:
            lit.doi = scienceDirect.getLitdoi(lit)
            lit.save()
        return



    def getRecomLitInfo(self):
        scienceDirect = ScienceDirect()
        RecLiterature_all_list = RecommendetLit.objects.all()
        for lit in RecLiterature_all_list:
                data = scienceDirect.getLitInfo(lit)
                if not (not data or "search-results" not in data or "service-error" in data or data==""):
                    print("heeeeeeeeeeee")
                    print(lit.doi)
                    searchResult = data["search-results"]
                    searchResult2 = searchResult["entry"]
                    for u in searchResult2:
                        if not ("error" in u or "AUTHENTICATION_ERROR" in u):
                            #if "prism:doi" in u:
                             #   lit.doi = u["prism:doi"]
                            if "citedby-count" in u:
                                lit.citation_count = u["citedby-count"]
                            if "openaccess" in u:
                                lit.Access_Type = u["openaccess"]
                             # we have to midify the year or date field in the model
                           # if "prism:coverDate" in u:
                            #    lit.Year = u["prism:coverDate"]
                            if "prism:volume" in u:
                                lit.Volume = u["prism:volume"]
                            if "affiliation" in u:
                                u1 = u["affiliation"]
                                for s in u1:
                                    lit.affiliation =s["affilname"]
                                    lit.affiliation_city =s["affiliation-city"]
                                    lit.affiliation_country =s["affiliation-country"]
                                    lit.save()

        return


    def getMendeleyfulldata(self):
        scienceDirect = ScienceDirect()
        RecLiterature_all_list = LiteratureCl.objects.all()
        #RecLiterature_all_list = RecommendetLit.objects.filter(id__lte=45, id__gte=45)
        #RecLiterature_all_list = LiteratureCl.objects.filter(id__lte=5857, id__gte=5001)

        for lit in RecLiterature_all_list:
            mendeley_id = scienceDirect.getMendeleyid(lit)
            if not (mendeley_id is None):
              # print(mendeley_id)
               print(lit.id)
               scienceDirect.getMendeleydata(mendeley_id,lit)
        return

    def getauthorsdata_byid(self):
        scienceDirect = ScienceDirect()
        Mendeleyauth_all_list = Authorsmendely.objects.all()

        for med_lit in Mendeleyauth_all_list:
            scienceDirect.fillauthosdata(med_lit)

        return


 # get citation count for recomLiterature
    def citationrecomLiterature(self):
        scienceDirect = ScienceDirect()
        #RecLiterature_all_list = LiteratureCl.objects.all()
        RecLiterature_all_list = LiteratureCl.objects.filter(id__lte=100, id__gte=1)
        for lit in RecLiterature_all_list:
            print(lit.id)
            if lit.doi is "":
                lit.citation_count = 0
            if lit.doi is None:
                lit.citation_count = 0
            else:
                lit.citation_count = scienceDirect.getCitationCount2(lit)
            lit.save()
        return


    def plumxsaveforRec(self):
       scienceDirect = ScienceDirect()


       RecLiterature_all_list = LiteratureCl.objects.filter(id__lte=5857, id__gte=2027)
       #RecLiterature_all_list = LiteratureCl.objects.all()

       for lit in RecLiterature_all_list:
           print(lit.id)
           scienceDirect.getPlumxdata(lit)
       return


    def altmetricssaveforRec(self):
           scienceDirect = ScienceDirect()
           #RecLiterature_all_list = RecommendetLit.objects.all()
           #RecLiterature_all_list = RecommendetLit.objects.filter(id__lte=46, id__gte=45)
           RecLiterature_all_list = LiteratureCl.objects.all()

           for lit in RecLiterature_all_list:
               scienceDirect.getAltmetricsdata(lit)
           return

    def getLitdoiIeee(self):
        scienceDirect = ScienceDirect()
        Literature_all_list = LiteratureCl.objects.all()
        for lit in Literature_all_list:
            print(lit.Title)
            if lit.doi is None:
                 lit.doi = scienceDirect.IeeegetDoi(lit.Title)
                 lit.save()
        return

    def getauthorGender(self):
        scienceDirect = ScienceDirect()
        #Authors_all_list = Authors.objects.all()
        Authors_all_list = Authors.objects.filter(id__lte=19551, id__gte=17977)

        for auth in Authors_all_list:
            if auth.name_given is not None:
                if ' ' in auth.name_given:
                   authname_list = auth.name_given.split(' ')
                   gender_auth = scienceDirect.getGender(authname_list[0],auth.name_surname)
                   if gender_auth is not None:
                       auth.augender = gender_auth
                       auth.save()
                else:
                    gender_auth = scienceDirect.getGender(auth.name_given, auth.name_surname)
                    if gender_auth is not None:
                        auth.augender = gender_auth
                        auth.save()
        return

    def getauthornumber(self):
        Authors_all_list = Authors.objects.all()
        LiteratureCl_all_list = LiteratureCl.objects.all()
        #LiteratureCl_all_list = LiteratureCl.objects.filter(id__lte=8335, id__gte=10)
        i=0
        for lit in LiteratureCl_all_list:
            i=1
            Authors_all_list = Authors.objects.filter(literature_id=lit)
            for auth in Authors_all_list:
               auth.eid = i
               auth.save()
               i = i+1

        return


    def getgender(self):
        scienceDirect = ScienceDirect()
        #print(classify_gender('john'))
        scienceDirect.getGender('james','smith')
        return




    def getpaperdoi(self):
        scienceDirect = ScienceDirect()
        RecommendetLit_all_list = RecommendetLit.objects.filter(Year__lte=1989, Year__gte=1978)
        for lit in RecommendetLit_all_list:
            print(lit.Year)
            lit.doi = scienceDirect.getLitdoi(lit)
            lit.save()
        return


    def getauthorsidfromtable(self):
        # save authors ids in classified!
        lit_with_samedoi =[]
        RecommendetLit_all_list = RecommendetLit.objects.filter(Year__lte=2021, Year__gte=1990)
        for litrec in RecommendetLit_all_list:
            lit = LiteratureCl.objects.filter(doi=litrec.doi).first()
            if lit is not None:
              lit_with_samedoi.append(lit)

        RecommendetLit_all_list2 = RecommendetLit.objects.filter(Year__lte=2021, Year__gte=1990)
        for litrec2 in RecommendetLit_all_list2:
            for lititem in lit_with_samedoi:
                if  litrec2.doi==lititem.doi:
                    print(lititem.AuthorsID)
                    litrec2.classified = lititem.AuthorsID
                    litrec2.save()
        return

    def getauthorsidfromsame_title(self):
        # save authors ids in classified!
        lit_with_samedoi = []
        RecommendetLit_all_list = RecommendetLit.objects.filter(classified="")
        for litrec in RecommendetLit_all_list:
            lit = LiteratureCl.objects.filter(Title=litrec.Title.lower()).first()
            if lit is not None:
                print(lit.id)
                litrec.classified = lit.AuthorsID
                litrec.save()
        return



    @staticmethod
    def splitAuthersinlist(auther_str, reliterature):
        if "," in auther_str:
           authers_list = auther_str.split(',')
           i = 0
           for auth in authers_list:
               # we will save the icse NEU authors temporary here
               author_m = Recomclassification()
               author_m.name = auth
               print(auth)
               author_m.RecommendetLit_id = reliterature
               author_m.save()
               i = i + 1
        elif "," not in auther_str:
            author_m = Recomclassification()
            author_m.name = auther_str
            print(auther_str)
            author_m.RecommendetLit_id = reliterature
            author_m.save()

        return


    def getauthorsidfrom_authersname(self):
        # save authors ids in classified!
        authorsnames = []
        temp_auth_id_list=''
        RecommendetLit_all_list = RecommendetLit.objects.filter(classified__isnull=True)
        Authors_all_list = Authors.objects.all()
        for litrec in RecommendetLit_all_list:
            print(litrec.Author)
            if "," in litrec.Author:
                authers_list = litrec.Author.split(',')
                for auth in authers_list:
                    for autht in Authors_all_list:
                        if auth == (autht.name_given + " " + autht.name_surname):
                            temp_auth_id_list += str(autht.scopus_author_id) + ","
                            break

                    litrec.classified = temp_auth_id_list
                    print(temp_auth_id_list)
                    litrec.save()
            elif "," not in litrec.Author:
                    for autht in Authors_all_list:
                        if litrec.Author == (autht.name_given + " " + autht.name_surname):
                            temp_auth_id_list += str(autht.scopus_author_id) + ","
                            break
                    print(temp_auth_id_list)
                    litrec.classified = temp_auth_id_list
                    litrec.save()
            temp_auth_id_list= ''

        return


    def fillauthosmissingIds(self):
        scienceDirect = ScienceDirect()
        #Lit_all_list = LiteratureCl.objects.all()
        Lit_all_list = LiteratureCl.objects.filter(id__lte=10862, id__gte=8001)

        for litrec in Lit_all_list:
            print(litrec.id)
            litrec.AuthorsID =scienceDirect.fillauthosmissingIds_scopus(litrec)
            litrec.save()
        return

    def fillauthosmissingIds_bytitle(self):
        scienceDirect = ScienceDirect()
        i=0
        RecommendetLit_all_list = LiteratureCl.objects.filter(AuthorsID__isnull=True)
        #RecommendetLit_all_list = LiteratureCl.objects.all()
        for litrec in RecommendetLit_all_list:
            if litrec.AuthorsID is None:
                print(litrec.id)
                AuthorsID_temp  =scienceDirect.fillauthosmissingIds_scopus_bytitle(litrec)
                print(AuthorsID_temp)
                if AuthorsID_temp is not None:
                    if AuthorsID_temp != "":
                       litrec.AuthorsID =AuthorsID_temp
                       litrec.save()
        return

    def fillauthosmissingIds_bydois(self):
        scienceDirect = ScienceDirect()
        i = 0
        RecommendetLit_all_list = LiteratureCl.objects.filter(id__lte=10862, id__gte=602)
        #RecommendetLit_all_list = LiteratureCl.objects.all()
        for litrec in RecommendetLit_all_list:
            if litrec.AuthorsID =="":
                print(litrec.id)
                AuthorsID_temp = scienceDirect.fillauthosmissingIds_scopus_bytitle(litrec)
                print(AuthorsID_temp)
                if AuthorsID_temp is not None:
                   if AuthorsID_temp != "":
                        litrec.AuthorsID = AuthorsID_temp
                        litrec.save()
        return

    def fillauthosmissingIds_DOIISNULL(self):
        scienceDirect = ScienceDirect()
        i = 0
        # RecommendetLit_all_list = LiteratureCl.objects.filter(AuthorsID__isnull=True)
        RecommendetLit_all_list = LiteratureCl.objects.all()
        for litrec in RecommendetLit_all_list:
            if litrec.doi is None:
                print(litrec.id)
                print(litrec.AuthorsID)
                AuthorsID_temp = scienceDirect.fillauthosmissingIds_scopus_bytitle(litrec)
                print(AuthorsID_temp)
                #if AuthorsID_temp is not None:
                 #   if AuthorsID_temp != "":
                  #      litrec.AuthorsID = AuthorsID_temp
                   #     litrec.save()
        return

    def savecoviddocsExcInTable(self):
        with open('scopus.csv', newline='', encoding = "ISO-8859-1") as csvfile:
            csv_data = csv.reader(csvfile, delimiter=',')
            line_count = 0
            for row in csv_data:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count = line_count + 1

                else:
                    line_count = line_count + 1
                    lCi = LiteratureCl()
                    lCi.Title  = row[2]
                    lCi.Author = row[0]
                    lCi.AuthorsID = row[1]
                    lCi.Year = row[3]
                    if row[4] != '':
                        lCi.Source =row[4]
                    if row[12] != '':
                        lCi.doi = row[12]
                    if row[13] != '':
                        lCi.url = row[13]
                    if row[11] != '':
                        lCi.citation_count = row[11]
                    if row[9] != '':
                        lCi.Affiliations = row[9]
                    if row[15] != '':
                        lCi.Document_Type =row[15]
                    if row[17] != '':
                        lCi.Publication_Stage = row[17]
                    if row[11] != '':
                        lCi.Access_Type = row[11]
                    lCi.save(force_insert=True)
                    print('post print:', lCi.Title, lCi.doi)
                    self.makeTokens(lCi.Title, WordType.TITLE.name, lCi)
                # if 'abstract' in entry:
                #   self.makeTokens(literature.abstract, WordType.ABSTRACT.name, literature)
                # if 'keywords' in entry:
                #   self.makeTokens(literature.keywords, WordType.KEYWORD.name, literature)
                # if 'author' in entry:
                #  self.splitAuthers(literature.author, literature, literature.year)
        return


    @staticmethod
    def getsingleIdAuthor(authorname):
        scienceDirect = ScienceDirect()
        print(authorname)
        if "." in authorname:
            authlist = authorname.split(" ", 2)
            print(authlist)
            if len(authlist) >2:
               AuthorsID_temp = scienceDirect.getauthorIDfromName(authlist[0]+" "+authlist[1], authlist[2])
               if AuthorsID_temp is not None:
                  print(AuthorsID_temp)
                  return AuthorsID_temp
            else:
                AuthorsID_temp = scienceDirect.getauthorIDfromName(authlist[0] , authlist[1])
                if AuthorsID_temp is not None:
                    print(AuthorsID_temp)
                    return AuthorsID_temp
        else:  # bbb bbb
            authlist = authorname.split(" ")
            if len(authlist) == 2:
                AuthorsID_temp = scienceDirect.getauthorIDfromName(authlist[0], authlist[1])
                if AuthorsID_temp is not None:
                   print(AuthorsID_temp)
                   return AuthorsID_temp
            else:
                AuthorsID_temp = scienceDirect.getauthorIDfromName(authlist[0]+" "+authlist[1], authlist[2])
                if AuthorsID_temp is not None:
                    print(AuthorsID_temp)
                    return AuthorsID_temp

        return

    def getauthorIDsfromNAMES(self):
        scienceDirect = ScienceDirect()
        i = 0
        RecommendetLit_all_list = LiteratureCl.objects.filter(id__lte=10294, id__gte=6000)
        #RecommendetLit_all_list = LiteratureCl.objects.filter(AuthorsID__isnull=True)

        for litrec in RecommendetLit_all_list:
            if litrec.AuthorsID =="missing ids":
                print(litrec.id)
                if litrec.Author.count(",")==0:
                    auid = self.getsingleIdAuthor(litrec.Author)
                    if auid is not None:
                       if auid != "":
                          litrec.AuthorsID = auid
                          litrec.save()
                elif litrec.Author.count(",")>0:
                     authlist = litrec.Author.split(",")
                     auidtemp=""
                     countids=0
                     for authorname in authlist:
                        auid = self.getsingleIdAuthor(authorname)
                        if auid is not None:
                            if auid != "":
                                auidtemp += auid+","
                                countids+=1
                     if countids == len(authlist):
                        print(auidtemp)
                        litrec.AuthorsID = auidtemp
                        litrec.save()
                     else:
                         print("missing ids")
                         litrec.AuthorsID = auidtemp
                         litrec.url="missing id"
                         litrec.save()

        return
#Authors reputation functions
    @staticmethod
    def papersMT():

        # authid = "https://dblp.uni-trier.de/pid/119/0420.html"
        conf = "icse"
        RecommendetLit_all_list = LiteratureCl.objects.filter(AbbreviatedSource=conf, Issue=1,
                                                              Pagecount__gte=7)
        count = RecommendetLit_all_list.count()
        print(count)
        return count
    @staticmethod
    def get_authorall_papers(authid,conf,year):

        #authid = "https://dblp.uni-trier.de/pid/119/0420.html"
        #conf = "icse"
        RecommendetLit_all_list = LiteratureCl.objects.filter(AuthorsID=authid,AbbreviatedSource=conf,Issue=0,Year__lte=year)
        count1 = RecommendetLit_all_list.count()
        RecommendetLit_all_list2 = LiteratureCl.objects.filter(AuthorsID=authid,AbbreviatedSource=conf,Issue=1,Pagecount__lte=6,Year__lte=year)
        count2 = RecommendetLit_all_list2.count()

        #for litrec in RecommendetLit_all_list:
        return count1+count2

    @staticmethod
    def get_authorall_MT_papers(authid,conf,year):

        #authid = "https://dblp.uni-trier.de/pid/119/0420.html"
        #conf = "icse"
        RecommendetLit_all_list = LiteratureCl.objects.filter(AuthorsID=authid,AbbreviatedSource=conf,Issue=1,Pagecount__gte=7,Year__lte=year)
        count = RecommendetLit_all_list.count()
        print(count)
        #for litrec in RecommendetLit_all_list:
        return count

    @staticmethod
    def get_authorall_MT_papers_fse(authid, conf, year):

        # authid = "https://dblp.uni-trier.de/pid/119/0420.html"
        # conf = "icse"
        RecommendetLit_all_list = LiteratureCl.objects.filter(AuthorsID=authid, AbbreviatedSource=conf, Issue=1,Year__lte=year)
        count = RecommendetLit_all_list.count()
        print(count)
        # for litrec in RecommendetLit_all_list:
        return count

    def get_co_author_Reputation_MT_only(self):

        authid = "https://dblp.uni-trier.de/pid/13/1022.html"
        conf = "icse"

        RecommendetLit_all_list = LiteratureCl.objects.filter(id__lte=34454, id__gte=56,Issue=1,AbbreviatedSource="ase")
        print(RecommendetLit_all_list.count())

        for litrec in RecommendetLit_all_list:
            dois_list = LiteratureCl.objects.filter(doi=litrec.doi)
            print(litrec.doi)
            reputation=0
            for d in dois_list:
                if d.AuthorsID != litrec.AuthorsID:
                    print(d.AuthorsID)
                    all_MT_papers = self.get_authorall_MT_papers(d.AuthorsID, d.AbbreviatedSource,d.Year)
                    #all_MT_papers = self.get_authorall_MT_papers_fse(d.AuthorsID, d.AbbreviatedSource,d.Year)
                    print(all_MT_papers)
                    academic_pub_age =d.author_publ_age
                    #norm_academic_pub_age=academic_pub_age/54
                    #norm_academic_pub_age=academic_pub_age/43
                    norm_academic_pub_age = academic_pub_age /49
                    print(academic_pub_age)
                    a_reputation = (all_MT_papers)*norm_academic_pub_age
                    print(a_reputation)
                    reputation = reputation+a_reputation

            print(reputation)
            litrec.Access_Type = str(reputation)
            litrec.save()

        return

    def get_co_author_Reputation(self):

        authid = "https://dblp.uni-trier.de/pid/13/1022.html"
        conf = "icse"

        RecommendetLit_all_list = LiteratureCl.objects.filter(id__lte=34454, id__gte=20001,Issue=1,AbbreviatedSource="icse")
        print(RecommendetLit_all_list.count())

        for litrec in RecommendetLit_all_list:
            dois_list = LiteratureCl.objects.filter(doi=litrec.doi)
            print(litrec.doi)
            reputation=0
            for d in dois_list:
                if d.AuthorsID != litrec.AuthorsID:
                    print(d.AuthorsID)
                    all_papers = self.get_authorall_papers(d.AuthorsID, d.AbbreviatedSource,d.Year)
                    print(all_papers)
                    all_MT_papers = self.get_authorall_MT_papers(d.AuthorsID, d.AbbreviatedSource,d.Year)
                    print(all_MT_papers)
                    academic_pub_age =d.author_publ_age
                    norm_academic_pub_age=academic_pub_age/54
                    print(academic_pub_age)
                    a_reputation = (all_papers+all_MT_papers*2)*norm_academic_pub_age
                    print(a_reputation)
                    reputation = reputation+a_reputation

            print(reputation)
            litrec.EID= str(reputation)
            litrec.save()

        return


    def get_authorall_authors_paperscount(self):

        RecommendetLit_all_list = LiteratureCl.objects.filter(id__lte=34454, id__gte=1,AbbreviatedSource="ase")
        for litrec in RecommendetLit_all_list:
            authpapers = LiteratureCl.objects.filter(AuthorsID=litrec.AuthorsID, AbbreviatedSource=litrec.AbbreviatedSource)
            count = authpapers.count()
            # issn is   all papers
            # idl is mt papers
            litrec.issn = str(count)
            litrec.save()
            print(count)
        return count


    def get_authorall_authors_MTpaperscount(self):
        RecommendetLit_all_list = LiteratureCl.objects.filter(id__lte=34454, id__gte=1, AbbreviatedSource="fse",Issue=1)
        for litrec in RecommendetLit_all_list:
            authpapers = LiteratureCl.objects.filter(AuthorsID=litrec.AuthorsID, AbbreviatedSource=litrec.AbbreviatedSource,Issue=1)
            count = authpapers.count()
            # issn is   all papers
            # idl is mt papers
            litrec.idl = str(count)
            litrec.save()
            print(count)
        return count
####################new################

    @staticmethod
    def get_authorall_MT_papers_all_conf(authid, year):

        # authid = "https://dblp.uni-trier.de/pid/119/0420.html"
        # conf = "icse"
        RecommendetLit_all_list = LiteratureCl.objects.filter(AuthorsID=authid, Issue=1,
                                                              Pagecount__gte=7, Year__lte=year)
        count = RecommendetLit_all_list.count()
        #print(count)
        return count

    def get_paper_Reputation_MT_only_all_conf(self):

        RecommendetLit_all_list = LiteratureCl.objects.filter(id__lte=34454, id__gte=1, Issue=1)

        for litrec in RecommendetLit_all_list:
            dois_list = LiteratureCl.objects.filter(doi=litrec.doi)
            print(litrec.doi)
            reputation = 0
            for d in dois_list:
                if d.AuthorsID != litrec.AuthorsID:
                    #print(d.AuthorsID)
                    all_MT_papers = self.get_authorall_MT_papers_all_conf(d.AuthorsID, d.Year)
                    #print(all_MT_papers)
                    academic_pub_age = d.author_publ_age
                    # norm_academic_pub_age=academic_pub_age/54
                    # norm_academic_pub_age=academic_pub_age/43
                    norm_academic_pub_age = academic_pub_age / 54
                    #print(academic_pub_age)
                    a_reputation = (all_MT_papers) * norm_academic_pub_age
                    #print(a_reputation)
                    reputation = reputation + a_reputation

            print(reputation)
            # now i save the reputation of co-author (all conf MT) in issn
            litrec.issn = str(reputation)
            litrec.save()

        return


    ####### Yusra  Twitter paper

    def saveTwittercsvInTable(self):
        with open('Files/3venues.csv', newline='', encoding = "ISO-8859-1") as csvfile:
            csv_data = csv.reader(csvfile, delimiter=',')
            line_count = 0
            for row in csv_data:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count = line_count + 1

                else:
                    line_count = line_count + 1
                    lCi = LiteratureCl()
                    lCi.Title = row[0]
                    if row[1] != '':
                        lCi.Year = row[1]
                    if row[2] != '':
                        lCi.Source =row[2]
                    if row[3] != '':
                        lCi.citation_count = row[3]
                    if row[4] != '':
                        lCi.doi = row[4]
                    lCi.save(force_insert=True)
        return



    def saveYusraToolcsvInTable(self):
        with open('Files/SLR1.csv', newline='', encoding="ISO-8859-1") as csvfile:
            csv_data = csv.reader(csvfile, delimiter=',')
            line_count = 0
            for row in csv_data:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count = line_count + 1

                else:
                    line_count = line_count + 1
                    lCi = LiteratureCl()
                    lCi.Author = row[0]
                    lCi.Title = row[1]
                    if row[2] != '':
                        lCi.Year = row[2]
                    if row[3] != '':
                        lCi.Source = row[3]

                    if row[4] != '':
                        lCi.citation_count = row[4]
                    else:
                        lCi.citation_count = 0
                    if row[5] != '':
                        lCi.doi = row[5]

                    if row[6] != '':
                        lCi.Abstract = row[6]

                    if row[7] != '':
                        lCi.Autherkeywords = row[7]

                    if row[8] != '':
                        lCi.Affiliations = row[8]


                    lCi.save(force_insert=True)
        return