import json
import urllib
import urllib.request
from urllib.request import Request, urlopen
import requests

import urllib.parse
from ..models.sourceDate import SourceData
from ..models.literatureCl import LiteratureCl
from ..models.plumx import Plumx
from ..models.mendeley import Mendeley
import time
from urllib.error import URLError, HTTPError
#from mendeley import Mendeley
#from mendeley.session import MendeleySession
import flask
from flask import redirect, render_template, request, session
import yaml
import http.client
import json
from ..models.readerbycountry import Readerbycountry
from ..models.readerbysubarea import Readerbysubarea
from ..models.readerbysubdiscipline import Readerbysubdiscipline
from ..models.authorsmendely import Authorsmendely
from ..models.altmetrics import Altmetrics
from ..models.authorsaltmetrics import Authorsaltmetrics
import ssl
import urllib3



class ScienceDirect:

    apiKey = "8ae25cee98ba830956d895f6d2f46255"
    apiKey2 = "7f59af901d2d86f78a1fd60c1bf9426a"
    apikey3 ="6580d02a3c6cece63fd07a71153aa96e"
    apikey4 ="78623d718721cb4c33ba0e22f771c484"
    newapikey ="7b234f853f17933508c848a50784125b"

    url = "https://api.elsevier.com/content/search/sciencedirect?"
    url2 = "http://api.elsevier.com/content/serial/title?title="
    url3 = "https://api.elsevier.com/analytics/plumx/doi/"
    url_citation = "https://api.elsevier.com/content/abstract/citation-count?"
    url_citation2="http://api.elsevier.com/content/search/scopus?query=DOI("
    url_doi ="https://api.elsevier.com/content/search/scopus?query=title("
    url_doi_all ="https://api.elsevier.com/content/search/scopus?query=doi("
    url_author_info = "https://api.elsevier.com/content/author?author_id="
    plumxeid_url ="https://api.elsevier.com/analytics/plumx/elsevier_id/"

    mendelyUrl="https://api.mendeley.com/catalog?doi=10.1103/PhysRevA.20.1521"
    altmetris_url = "https://api.altmetric.com/v1/doi/"
    ieee_url = "https://ieeexploreapi.ieee.org/api/v1/search/articles?apikey=mdfhu5auy9ktc28z9p499ez5&article_title="

    getVars = {'apiKey': apiKey}
    getVars2 = {'apiKey': apiKey2}
    getVars3 = {'apiKey': apikey3}
    getVars4 = {'apiKey': apikey4}



    # Get citation count
    def getCitationCount(self, lit):
        doi_lit = lit.getDoiOnly()
        self.getVars2["doi"] = doi_lit
        time.sleep(7)
        requestUrl = self.url_citation + urllib.parse.urlencode(self.getVars2)
        print(requestUrl)
        r = urllib.request.urlopen(requestUrl)
        data = json.load(r)
        if not data:
            return None
        if "citation-count-response" not in data:
            return 0
        print(requestUrl)
        searchResult = data["citation-count-response"]
        searchResult2 = searchResult["document"]
        if "citation-count" not in searchResult2:
            return 0
        else:
            cotationCount = searchResult2["citation-count"]
        return cotationCount



        # Get citation count request new
    def getCitationCount2(self, lit):
            hdr = {'X-ELS-APIKey': '8ae25cee98ba830956d895f6d2f46255'}
            doi_lit = lit.getDoiOnly()
            time.sleep(6)
            requestUrl = self.url_citation2 + doi_lit+")&apiKey=8ae25cee98ba830956d895f6d2f46255&field=citedby-count"
            print(requestUrl)
            req = urllib.request.Request(requestUrl)
            response = urllib.request.urlopen(req)
            data = json.load(response)
            print(data)
            if not data:
                return None
            if "search-results" not in data:
                return 0
            searchResult = data["search-results"]
            searchResult2 = searchResult["entry"]
            cotationCount = 0
            for u in searchResult2:
                if "citedby-count" in u:
                    cotationCount = u["citedby-count"]
            return cotationCount



    # Get the number of document by author first + last name
    def getDocumentCountByAuthor(self, firstName,lastName):
        fullName = firstName + " " + lastName
        self.getVars["query"] = "author(\"\\\"" + fullName + "\\\"\")"
        requestUrl = self.url + urllib.parse.urlencode(self.getVars)
        print(requestUrl)
        r = urllib.request.urlopen(requestUrl)
        data = json.load(r)
        searchResult = data["search-results"]
        resultCount = searchResult["opensearch:totalResults"]
        return resultCount


    #Get source data (journal in science direct) from scopus
    def getSourcedataScopus(self, journal_title):
        journal_title_n = journal_title.replace("&", "and")
        self.getVars3["title"] = journal_title_n
        time.sleep(5)
        print(journal_title)

        u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
        requestUrl = self.url2 + journal_title_n+"&apiKey=6580d02a3c6cece63fd07a71153aa96e"
        print(requestUrl)
        response = requests.get(requestUrl, headers={"USER-AGENT": u_a})
        data = response.json()  # ['search-results']
        if not data:
          return None
        if "error" in data:
            return None
        else:
            print(data)
        #r = urllib.request.urlopen(requestUrl)
        #data = json.load(r)
        #print("-----")
        #if not data:
         #   return None
            source = SourceData()
            sourceDataList = source.parseSourceDataArrayFromJson(data,journal_title_n)
            if not sourceDataList:
             return None
            else:
                  print("Now")
                  for i in sourceDataList:
                      print(i.citeScoreTracker)
                      print(i.citeScoreCurrentMetric)
                      print(i.SJRList[0])
                      print(i.SNIPList[0])
                      print("\n")
        # print("Now")
        return sourceDataList

    # Get the number of document by author full name
    def getDocumentCountByAuthorFullname(self, fullName):
            self.getVars3["query"] = "author(\"\\\"" + fullName + "\\\"\")"
            time.sleep(7)
            requestUrl = self.url + urllib.parse.urlencode(self.getVars3)
            print(requestUrl)
            r = urllib.request.urlopen(requestUrl)
            data = json.load(r)
            searchResult = data["search-results"]
            resultCount = searchResult["opensearch:totalResults"]
            return resultCount

 #Get plumx data (journal in science direct) from scopus
    def getPlumxdata(self,lit):
        if lit.doi is "":
            return
        if lit.doi is None:
            return
        else:
            doi_lit = lit.getDoiOnly()
            #doi_lit="10.1056/NEJMoa2002032"
            requestUrl = self.url3 + doi_lit + "?" + urllib.parse.urlencode(self.getVars2)
            #print(requestUrl)
            # good doi example
            # DOI: 10.1016/j.compedu.2012.03.004
            #requestUrl = self.url3 + "10.1016/j.compedu.2012.03.004?" + urllib.parse.urlencode(self.getVars2)
            #print(requestUrl)

            req = Request(requestUrl)
            try:
                r = urlopen(req)
               # print("i am here")
            except HTTPError as e:
                print('The server couldnt fulfill the request.')
                print('Error code: ', e.code)
            except URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            else:
            #r = urllib.request.urlopen(requestUrl)
                data = json.load(r)
                if not data:
                    return None
                if "errorCode" in data:
                    return None

                if len(data) == 0:
                    return []
                if "count_categories" not in data:
                    return None

                plumx = Plumx()
                plumx.Literature_id = lit
                # save for the rec
                #plumx.recLiterature_id = lit
                resultListOfplumxData = []
                root = data["count_categories"]
                i=0

                while i < len(root):
                 result = root[i]
                 if result["name"] == "capture":
                   plumx.Capture_count=result["total"]
                   searchResult = result["count_types"]
                   for s in searchResult:
                       if s["name"] == "READER_COUNT":
                           plumx.Reader_count = s["total"]
                       if s["name"] == "EXPORTS_SAVES":
                           plumx.export_save = s["total"]
                       if s["name"] == "BOOKMARK_COUNT":
                           plumx.Book_mark_count = s["total"]
                       if s["name"] == "DOWNLOAD_COUNT":
                           plumx.download_ct = s["total"]
                 if result["name"] == "citation":
                      plumx.Citation_count=result["total"]
                      searchResult = result["count_types"]
                      for s in searchResult:
                         if s["name"] == "CITED_BY_COUNT":
                             plumx.cited_by_count = s["total"]
                             searchResult = s["sources"]
                             for s in searchResult:
                                if s["name"] == "Scopus":
                                   plumx.Scopus_cit_count = s["total"]
                                if s["name"] == "CrossRef":
                                   plumx.Crossref = s["total"]
                                if s["name"] == "SSRN":
                                    plumx.SSRN = s["total"]
                                if s["name"] == "PubMedCentralEurope":
                                    plumx.PubMedCentralEurope = s["total"]
                                if s["name"] == "PubMed":
                                   plumx.pubmed = s["total"]
                                if s["name"] == "Academic Citation Index (ACI) - airiti":
                                   plumx.Aci_cit = s["total"]
                                if s["name"] =="SciELO":
                                   plumx.SciELO = s["total"]
                         if s["name"] == "CLINICAL_CITED_BY_COUNT":
                             plumx.Clinical_citedby_count = s["total"]
                             plumx.Clinical_citedby_count_sources = s["sources"]
                             searchResult1 = s["sources"]
                             for s in searchResult1:
                                if s["name"] == "PubMed Guidelines":
                                   plumx.PubMed_Guidelines_cot = s["total"]
                                if s["name"] == "DynaMed Plus":
                                    plumx.DynaMed_Plus = s["total"]
                                if s["name"] == "NICE":
                                    plumx.NICE = s["total"]
                         if s["name"] =="PATENT_FAMILY_COUNT" :
                             plumx.patentfam_count = s["total"]
                             plumx.patentfam_count_sources = s["sources"]
                             searchResult1 = s["sources"]
                             for s in searchResult1:
                                 if s["name"] == "Patent Families":
                                     plumx.Patent_families = s["total"]
                         if s["name"] =="POLICY_CITED_BY_COUNT" :
                             plumx.policy_count = s["total"]
                             searchResult1 = s["sources"]
                             for s in searchResult1:
                                 if s["name"] == "Policy Citation":
                                     plumx.Policy_citation = s["total"]
                 if result["name"] == "mention":
                      plumx.Mention_count = result["total"]
                      searchResult = result["count_types"]
                      for s in searchResult:
                         if s["name"] == "NEWS_COUNT":
                            plumx.News_count = s["total"]
                         if s["name"] == "ALL_BLOG_COUNT":
                            plumx.Blog_count = s["total"]
                         if s["name"] == "QA_SITE_MENTIONS":
                            plumx.QA_site_mentioncount = s["total"]
                         if s["name"] == "REFERENCE_COUNT":
                            plumx.reference_count = s["total"]
                         if s["name"] == "LINK_COUNT":
                            plumx.link_count = s["total"]
                         if s["name"] == "COMMENT_COUNT":
                             plumx.Comment_count = s["total"]
                 if result["name"] == "socialMedia":
                      plumx.Social_count=result["total"]
                      searchResult = result["count_types"]
                      for s in searchResult:
                          if s["name"] =="TWEET_COUNT":
                             plumx.Tweet_count = s["total"]
                          if s["name"] == "FACEBOOK_COUNT":
                             plumx.FB_count = s["total"]
                 if result["name"] == "usage":
                      plumx.Usage_count=result["total"]
                      searchResult = result["count_types"]
                      for s in searchResult:
                          if s["name"] == "ABSTRACT_VIEWS":
                             plumx.abstract_view = s["total"]
                          if s["name"] == "LINK_CLICK_COUNT":
                             plumx.link_click_count = s["total"]
                          if s["name"] == "FULL_TEXT_VIEWS":
                             plumx.Fulltxt_viw = s["total"]
                          if s["name"] == "LINK_OUTS":
                             plumx.link_out = s["total"]
                          if s["name"] == "DOWNLOAD_COUNT":
                             plumx.download_ct = s["total"]
                 i += 1
                 plumx.save()
            return



# get pLUMX data using Elsevir id for lit without doi

    def getPlumxdataElsv(self,litEID,lit):

        requestUrl = self.plumxeid_url + litEID + "?" + urllib.parse.urlencode(self.getVars2)
        print(requestUrl)
        req = Request(requestUrl)
        try:
            r = urlopen(req)
            print("i am here")
        except HTTPError as e:
            print('The server couldnt fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        else:
        #r = urllib.request.urlopen(requestUrl)
            data = json.load(r)
            if not data:
                return None
            if "errorCode" in data:
                return None

            if len(data) == 0:
                return []
            if "count_categories" not in data:
                return None

            plumx = Plumx()
            plumx.Literature_id = lit
            # save for the rec
            #plumx.recLiterature_id = lit
            resultListOfplumxData = []
            root = data["count_categories"]
            i=0

            while i < len(root):
             result = root[i]
             if result["name"] == "capture":
               plumx.Capture_count=result["total"]
               searchResult = result["count_types"]
               for s in searchResult:
                   if s["name"] == "READER_COUNT":
                       plumx.Reader_count = s["total"]
                   if s["name"] == "EXPORTS_SAVES":
                       plumx.export_save = s["total"]
                   if s["name"] == "BOOKMARK_COUNT":
                       plumx.Book_mark_count = s["total"]
                   if s["name"] == "DOWNLOAD_COUNT":
                       plumx.download_ct = s["total"]
             if result["name"] == "citation":
                  plumx.Citation_count=result["total"]
                  searchResult = result["count_types"]
                  for s in searchResult:
                     if s["name"] == "CITED_BY_COUNT":
                         plumx.cited_by_count = s["total"]
                         searchResult = s["sources"]
                         for s in searchResult:
                            if s["name"] == "Scopus":
                               plumx.Scopus_cit_count = s["total"]
                            if s["name"] == "CrossRef":
                               plumx.Crossref = s["total"]
                            if s["name"] == "SSRN":
                                plumx.SSRN = s["total"]
                            if s["name"] == "PubMedCentralEurope":
                                plumx.PubMedCentralEurope = s["total"]
                            if s["name"] == "PubMed":
                               plumx.pubmed = s["total"]
                            if s["name"] == "Academic Citation Index (ACI) - airiti":
                               plumx.Aci_cit = s["total"]
                            if s["name"] =="SciELO":
                               plumx.SciELO = s["total"]
                     if s["name"] == "CLINICAL_CITED_BY_COUNT":
                         plumx.Clinical_citedby_count = s["total"]
                         plumx.Clinical_citedby_count_sources = s["sources"]
                         searchResult1 = s["sources"]
                         for s in searchResult1:
                            if s["name"] == "PubMed Guidelines":
                               plumx.PubMed_Guidelines_cot = s["total"]
                            if s["name"] == "DynaMed Plus":
                                plumx.DynaMed_Plus = s["total"]
                            if s["name"] == "NICE":
                                plumx.NICE = s["total"]
                     if s["name"] =="PATENT_FAMILY_COUNT" :
                         plumx.patentfam_count = s["total"]
                         plumx.patentfam_count_sources = s["sources"]
                         searchResult1 = s["sources"]
                         for s in searchResult1:
                             if s["name"] == "Patent Families":
                                 plumx.Patent_families = s["total"]
                     if s["name"] =="POLICY_CITED_BY_COUNT" :
                         plumx.policy_count = s["total"]
                         searchResult1 = s["sources"]
                         for s in searchResult1:
                             if s["name"] == "Policy Citation":
                                 plumx.Policy_citation = s["total"]
             if result["name"] == "mention":
                  plumx.Mention_count = result["total"]
                  searchResult = result["count_types"]
                  for s in searchResult:
                     if s["name"] == "NEWS_COUNT":
                        plumx.News_count = s["total"]
                     if s["name"] == "ALL_BLOG_COUNT":
                        plumx.Blog_count = s["total"]
                     if s["name"] == "QA_SITE_MENTIONS":
                        plumx.QA_site_mentioncount = s["total"]
                     if s["name"] == "REFERENCE_COUNT":
                        plumx.reference_count = s["total"]
                     if s["name"] == "LINK_COUNT":
                        plumx.link_count = s["total"]
                     if s["name"] == "COMMENT_COUNT":
                         plumx.Comment_count = s["total"]
             if result["name"] == "socialMedia":
                  plumx.Social_count=result["total"]
                  searchResult = result["count_types"]
                  for s in searchResult:
                      if s["name"] =="TWEET_COUNT":
                         plumx.Tweet_count = s["total"]
                      if s["name"] == "FACEBOOK_COUNT":
                         plumx.FB_count = s["total"]
             if result["name"] == "usage":
                  plumx.Usage_count=result["total"]
                  searchResult = result["count_types"]
                  for s in searchResult:
                      if s["name"] == "ABSTRACT_VIEWS":
                         plumx.abstract_view = s["total"]
                      if s["name"] == "LINK_CLICK_COUNT":
                         plumx.link_click_count = s["total"]
                      if s["name"] == "FULL_TEXT_VIEWS":
                         plumx.Fulltxt_viw = s["total"]
                      if s["name"] == "LINK_OUTS":
                         plumx.link_out = s["total"]
                      if s["name"] == "DOWNLOAD_COUNT":
                         plumx.download_ct = s["total"]
             i += 1
             plumx.save()
            return



        # Get doi for recommendations
    def getLitdoi(self, lit):
            hdr = {'X-ELS-APIKey': '37ee5ee05ca81a4b87f5f1bd5f141213'}

            u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
           # response = requests.get(url, headers={"USER-AGENT": u_a})
            title_lit = lit.getTitle()
            requestUrl = self.url_doi + title_lit + ")&apiKey=37ee5ee05ca81a4b87f5f1bd5f141213"
            response = requests.get(requestUrl, headers={"USER-AGENT": u_a})
            data = response.json()#['search-results']
            if not data:
                return None
            if "search-results" not in data:
                return 0
            else:
    #this needs to be tested and get the dois again upon exact equality btw title
                searchResult = data["search-results"]
                searchResult2 = searchResult["entry"]
                for u in searchResult2:
                    if "error" in u:
                       return None
                    else:
                        dc_title = u["dc:title"] + ".,"
                        if title_lit.lower() == dc_title.lower():
                            print("Inside")
                            if "prism:doi" in u:
                                  doi = u["prism:doi"]
                                  print(doi)
                                  return doi


     # Get doi for recommendations
    def getLitcitNew(self, doi):

            u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
           # response = requests.get(url, headers={"USER-AGENT": u_a})
            requestUrl = self.url_doi_all + doi + ")&apiKey=8ae25cee98ba830956d895f6d2f46255"
            print(requestUrl)
            response = requests.get(requestUrl, headers={"USER-AGENT": u_a})
            data = response.json()#['search-results']
            if not data:
                return None
            if "search-results" not in data:
                return 0
            else:
                searchResult = data["search-results"]
                searchResult2 = searchResult["entry"]
                for u in searchResult2:
                    if "error" in u:
                       return None
                    else:
                        #dc_title = u["dc:title"] + ".,"
                        #if title_lit.lower() == dc_title.lower():
                        if "citedby-count" in u:
                            cit = u["citedby-count"]
                            print(cit)
                            return cit

    def getLitcitNewusingtitel(self, title_lit):

        headers = {
            'Accept': 'application/json',
            'X-ELS-APIKey': '7b234f853f17933508c848a50784125b',
            'X-ELS-Insttoken': '0bbce5676be39b3e60c2199eadd68f97'
        }
        url1 = 'https://api.elsevier.com/content/search/scopus?query=title('
        url = url1 + title_lit + ")&view=COMPLETE"

        response = requests.get(url, headers=headers)

        data = response.json()
        if not data:
            return None
        if "service-error" in data:
            return None
        if "search-results" not in data:
            return 0
        else:
           searchResult = data["search-results"]
           searchResult2 = searchResult["entry"]
           for u in searchResult2:
                if "error" in u:
                    return None
                else:
                    dc_title = u["dc:title"] + "."
                    if title_lit.lower() == dc_title.lower():
                       if "citedby-count" in u:
                         cit = u["citedby-count"]
                         print(cit)
                         return cit



    def getLitInfo(self, lit):
        hdr = {'X-ELS-APIKey': '8ae25cee98ba830956d895f6d2f46255'}

        u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
        # response = requests.get(url, headers={"USER-AGENT": u_a})
        data = ""
        if not (lit.doi =="" or lit.doi is None):
            doi_lit = lit.doi
            requestUrl = self.url_doi_all + doi_lit + ")&apiKey=8ae25cee98ba830956d895f6d2f46255"
            print(requestUrl)
            response = requests.get(requestUrl, headers={"USER-AGENT": u_a})
            data = response.json()  # ['search-results']
            print(data)
        return data



    def getMendeleyid(self,lit):
        if lit.doi is "":
            return
        if lit.doi is None:
            return
        else:
            doi_lit = lit.getDoiOnly()
        conn = http.client.HTTPSConnection("api.mendeley.com")
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer MSwxNjA1NzA1NTY2NTU5LDU5NTU1MTIwMSwxMDI4LGFsbCwsLGZiMjFmMTI1M2FmYmE1NDRkYjA5MWQ0NmU3ZjM3M2JlM2EwY2d4cnFiLDUyNjJmNWIwLWVlN2EtMzZmOC05YTIwLWM1Mjg2MzAxOTVhMCx0QlgyRWt2ZlExZmFjb0FXLXFxb0VvemEzWTQ"
        }

        conn.request("GET", "/catalog?doi="+doi_lit, headers=headers)
        res = conn.getresponse()
        data = res.read()
        #print(data.decode("utf-8"))
        responseObjectjason = json.loads(data)
        for v in responseObjectjason:
            return str(v["id"])
        return


    def getMendeleydata(self,id,lit):
        conn = http.client.HTTPSConnection("api.mendeley.com")
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer MSwxNjA1NzA1NTY2NTU5LDU5NTU1MTIwMSwxMDI4LGFsbCwsLGZiMjFmMTI1M2FmYmE1NDRkYjA5MWQ0NmU3ZjM3M2JlM2EwY2d4cnFiLDUyNjJmNWIwLWVlN2EtMzZmOC05YTIwLWM1Mjg2MzAxOTVhMCx0QlgyRWt2ZlExZmFjb0FXLXFxb0VvemEzWTQ"
        }
        #id ="eaede082-7d8b-3f0c-be3a-fb7be685fbe6"
        conn.request("GET", "/catalog/"+id+"?view=stats", headers=headers)
        res = conn.getresponse()
        data = res.read()
        responseObjectjason = json.loads(data)
        #print(responseObjectjason)
        if not responseObjectjason:
            return None
        if "errorCode" in responseObjectjason:
            return None
        if len(responseObjectjason) == 0:
            return []
        mendely1 = Mendeley()
        #mendely1.recLiterature_id = lit
        mendely1.Literature_id = lit
        if "reader_count" in responseObjectjason:
            mendely1.reader_count = responseObjectjason["reader_count"]
        if "reader_count_by_academic_status" in responseObjectjason:
            mendely1.reader_count_by_academic_status = responseObjectjason["reader_count_by_academic_status"]
        if "reader_count_by_subject_area" in responseObjectjason:
            mendely1.reader_count_by_subject_area = responseObjectjason["reader_count_by_subject_area"]
        if "reader_count_by_subdiscipline" in responseObjectjason:
            mendely1.reader_count_by_subdiscipline = responseObjectjason["reader_count_by_subdiscipline"]
        if "reader_count_by_country" in responseObjectjason:
            mendely1.reader_count_by_country = responseObjectjason["reader_count_by_country"]
        if "reader_count_by_academic_status" in responseObjectjason:
           if "Student  > Postgraduate" in responseObjectjason["reader_count_by_academic_status"].keys():
               mendely1.StdPostgraduate_count = responseObjectjason["reader_count_by_academic_status"]["Student  > Postgraduate"]
           if "Professor > Associate Professor" in responseObjectjason["reader_count_by_academic_status"].keys():
               mendely1.ProfessorAssociatProf_count = responseObjectjason["reader_count_by_academic_status"]["Professor > Associate Professor"]
           if "Researcher" in responseObjectjason["reader_count_by_academic_status"].keys():
               mendely1.Researcher_count = responseObjectjason["reader_count_by_academic_status"]["Researcher"]
           if "Student  > Master" in responseObjectjason["reader_count_by_academic_status"].keys():
               mendely1.StdMaster_count = responseObjectjason["reader_count_by_academic_status"]["Student  > Master"]
           if "Student  > Ph. D. Student" in responseObjectjason["reader_count_by_academic_status"].keys():
               mendely1.StdPhd_count = responseObjectjason["reader_count_by_academic_status"]["Student  > Ph. D. Student"]
           if "Professor" in responseObjectjason["reader_count_by_academic_status"].keys():
               mendely1.Professor_count = responseObjectjason["reader_count_by_academic_status"]["Professor"]
           if "Student  > Bachelor" in responseObjectjason["reader_count_by_academic_status"].keys():
               mendely1.StdBachelor_count = responseObjectjason["reader_count_by_academic_status"]["Student  > Bachelor"]
           if "Student  > Doctoral Student" in responseObjectjason["reader_count_by_academic_status"].keys():
               mendely1.StdDoctoralstd_count = responseObjectjason["reader_count_by_academic_status"]["Student  > Doctoral Student"]
           if "Lecturer" in responseObjectjason["reader_count_by_academic_status"].keys():
               mendely1.Lecturer_count = responseObjectjason["reader_count_by_academic_status"]["Lecturer"]
           if "Other" in responseObjectjason["reader_count_by_academic_status"].keys():
               mendely1.Other_count = responseObjectjason["reader_count_by_academic_status"]["Other"]
           if "Librarian" in responseObjectjason["reader_count_by_academic_status"].keys():
               mendely1.Librarian_count = responseObjectjason["reader_count_by_academic_status"]["Librarian"]
           if "Lecturer > Senior Lecturer" in responseObjectjason["reader_count_by_academic_status"].keys():
               mendely1.LecturerSeniorLec_count = responseObjectjason["reader_count_by_academic_status"]["Lecturer > Senior Lecturer"]
           if "Unspecified" in responseObjectjason["reader_count_by_academic_status"].keys():
               mendely1.Unspecified_count = responseObjectjason["reader_count_by_academic_status"]["Unspecified"]
        if "group_count" in responseObjectjason:
            mendely1.group_count = responseObjectjason["group_count"]
        if "has_pdf" in responseObjectjason:
            mendely1.has_pdf = responseObjectjason["has_pdf"]
        mendely1.save()

        if "reader_count_by_country" in responseObjectjason:
            listofcountries = responseObjectjason["reader_count_by_country"]
            readerbycountry = Readerbycountry()
            readerbycountry.mendely_id = mendely1
            for k, v in listofcountries.items():
                #print("key:" + k + ", value:" + str(v))
                readerbycountry.countrtname = k
                readerbycountry.countrycount = v
                readerbycountry.save()

        if "reader_count_by_subject_area" in responseObjectjason:
            listofsubarea = responseObjectjason["reader_count_by_subject_area"]
            readerbysubarea = Readerbysubarea()
            readerbysubarea.mendely_id = mendely1
            for k, v in listofsubarea.items():
                #print("key:" + k + ", value:" + str(v))
                readerbysubarea.subname = k
                readerbysubarea.subcount = v
                readerbysubarea.save()

        if "reader_count_by_subdiscipline" in responseObjectjason:
            listofsubdis = responseObjectjason["reader_count_by_subdiscipline"]
            readerbysubdiscipline = Readerbysubdiscipline()
            readerbysubdiscipline.mendely_id = mendely1
            for k, v in listofsubdis.items():
                #print("key:" + k + ", value:" + v)
                readerbysubdiscipline.disname = k
                for key in v:
                    readerbysubdiscipline.discount = v[key]
                readerbysubdiscipline.save()

        # to be checked when doing the authors paper
        #if "authors" in responseObjectjason:
         #   listofauthors = responseObjectjason["authors"]
          #  for ent in listofauthors:
           #     authorsmendely = Authorsmendely()
            #    authorsmendely.mendely_id = mendely1
             #   authorsmendely.first_name = ent["first_name"]
              #  authorsmendely.last_name = ent["last_name"]
               # authorsmendely.scopus_author_id = ent["scopus_author_id"]
                #authorsmendely.save()

        return


    def fillauthosdata(self,menauth_lit):

        s_author_id = menauth_lit.scopus_author_id

        hdr = {'Accept': 'application/json'}

        time.sleep(6)

        requestUrl = self.url_author_info + s_author_id+"&apiKey=7f59af901d2d86f78a1fd60c1bf9426a"
        req = urllib.request.Request(requestUrl, headers=hdr)
        response = urllib.request.urlopen(req)
        data = json.load(response)
        if not data:
            return None
        if "author-retrieval-response" not in data:
            return 0
        searchResult = data["author-retrieval-response"]


        for k, v in searchResult.items():
            if k == "coredata":
                print("hiiiiii")


        if "coredata" in searchResult.keys():
            searchResult2 = searchResult["coredata"]
            for k, v in searchResult2.items():
                if k == "document-count":
                    menauth_lit.document_count = v
                if k == "cited-by-count":
                    menauth_lit.cited_by_count = v
                if k == "citation_count":
                    menauth_lit.citation_count = v

        if "author-profile" in searchResult:
            searchResult2 = searchResult["author-profile"]
            menauth_lit.name_indexed = searchResult2["preferred-name"]["indexed-name"]
            menauth_lit.name_initials = searchResult2["preferred-name"]["initials"]
            menauth_lit.name_surname = searchResult2["preferred-name"]["surname"]
            menauth_lit.name_given = searchResult2["preferred-name"]["given-name"]
        if "publication-range" in searchResult:
            searchResult2 = searchResult["publication-range"]
            menauth_lit.name_indexed = searchResult2["@end"]
            menauth_lit.name_initials = searchResult2["@start"]
            menauth_lit.save()

        return



    def getAltmetricsdata(self,lit):
        if lit.doi is "":
            return
        if lit.doi is None:
            return
        else:
            doi_lit = lit.getDoiOnly()
            #doi_lit = "10.1038/nrd.2017.244"
            requestUrl = self.altmetris_url + doi_lit
            print(requestUrl)
            req = Request(requestUrl)
            try:
                r = urlopen(req)
                print("i am here")
            except HTTPError as e:
                print('The server couldnt fulfill the request.')
                print('Error code: ', e.code)
            except URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            else:
                # r = urllib.request.urlopen(requestUrl)
                data = json.load(r)
                if not data:
                    return None
                if "errorCode" in data:
                    return None
                if len(data) == 0:
                    return []

                altmetrics = Altmetrics()
                #altmetrics.recLiterature_id = lit
                altmetrics.Literature_id = lit
                #altmetrics.altmetric_jid = data["altmetric_jid"]
                altmetrics.type = data["type"]
                altmetrics.altmetric_id = data["altmetric_id"]
                if "journal" in data:
                    altmetrics.journal = data["journal"]
                if "is_oa" in data:
                    altmetrics.is_oa = data["is_oa"]
                if "schema" in data:
                    altmetrics.schema = data["schema"]
                if "score" in data:
                    altmetrics.score = data["score"]
                if "cited_by_posts_count" in data:
                   altmetrics.cited_by_posts_count = data["cited_by_posts_count"]
                if "cited_by_msm_count" in data:
                   altmetrics.cited_by_msm_count = data["cited_by_msm_count"]
                if "cited_by_policies_count" in data:
                   altmetrics.cited_by_policies_count = data["cited_by_policies_count"]
                if "cited_by_tweeters_count" in data:
                   altmetrics.cited_by_tweeters_count = data["cited_by_tweeters_count"]
                if "cited_by_fbwalls_count" in data:
                   altmetrics.cited_by_fbwalls_count = data["cited_by_fbwalls_count"]
                if "cited_by_rh_count" in data:
                   altmetrics.cited_by_rh_count = data["cited_by_rh_count"]
                if "cited_by_patents_count" in data:
                   altmetrics.cited_by_patents_count = data["cited_by_patents_count"]
                if "cited_by_accounts_count" in data:
                   altmetrics.cited_by_accounts_count = data["cited_by_accounts_count"]
                if "last_updated" in data:
                   altmetrics.last_updated = data["last_updated"]
                if "added_on" in data:
                   altmetrics.added_on = data["added_on"]
                if "published_on" in data:
                   altmetrics.published_on = data["published_on"]
                if "readers_count" in data:
                   altmetrics.readers_count = data["readers_count"]
                altmetrics.citeulike_reader = data["readers"]["citeulike"]
                altmetrics.mendeley = data["readers"]["mendeley"]
                altmetrics.connotea = data["readers"]["connotea"]
                altmetrics.save()

                if "authors" in data:
                    listofauthors = data["authors"]
                    authorsaltmetrics = Authorsaltmetrics()
                    authorsaltmetrics.altmetrics_id =altmetrics
                    for k in listofauthors:
                        authorsaltmetrics.name = k
                        authorsaltmetrics.save()


        return




    def  fillauthosdata_scopus(self,auth_lit):

        s_author_id = auth_lit.scopus_author_id

        hdr = {'Accept': 'application/json',
               "USER-AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
        }

       # time.sleep(2)

        requestUrl = self.url_author_info + str(s_author_id)+"&apiKey=88c15e176b1d05748dc4485439d356c6&view=ENHANCED"
        req = urllib.request.Request(requestUrl, headers=hdr)
        #print(requestUrl)
        try:
            response = urllib.request.urlopen(req)
        except HTTPError as e:
            print('Error code: ', e.code)
        except URLError as e:
            print('Reason: ', e.reason)
        else:
            # r = urllib.request.urlopen(requestUrl)
            data = json.load(response)
            if not data:
                return None
            if "service-error" in data:
                return None
            searchResult = data["author-retrieval-response"]

            for k in searchResult:
                auth_lit.document_count = k["coredata"]["document-count"]
                auth_lit.cited_by_count = k["coredata"]["cited-by-count"]
                auth_lit.citation_count = k["coredata"]["citation-count"]
                # added in 12 Nov
                # here add the Hindex
                auth_lit.citation_all_count = k["h-index"]
                # here add the coAuthors
                auth_lit.lit_date = k["coauthor-count"]

                auth_lit.name_indexed = k["author-profile"]["preferred-name"]["indexed-name"]
                auth_lit.name_initials = k["author-profile"]["preferred-name"]["initials"]
                auth_lit.name_surname = k["author-profile"]["preferred-name"]["surname"]
                auth_lit.name_given = k["author-profile"]["preferred-name"]["given-name"]

                auth_lit.start_year = k["author-profile"]["publication-range"]["@start"]
                auth_lit.end_year = k["author-profile"]["publication-range"]["@end"]
                auth_lit.save()

        return



    def  fillauthosdata_scopustoken(self,auth_lit):

        s_author_id = auth_lit.scopus_author_id
        #mynewapiSunday = 7c871f796a8f3fc24c7364ede556527b

        hdr = {
            'Accept': 'application/json',
               'X-ELS-APIKey': '7b234f853f17933508c848a50784125b',
               'X-ELS-Insttoken': '0bbce5676be39b3e60c2199eadd68f97'
               }

        #time.sleep(6)
       #New token at 29 Nov
        headers = {
            'Accept': 'application/json',
            'X-ELS-APIKey': '88c15e176b1d05748dc4485439d356c6',
            'X-ELS-Insttoken': '0efaf4426dab0954258f1cb71281eeff'
        }
        url = 'https://api.elsevier.com/content/author'
        # Today is 12 Nov we added this to get the h-index and co-author count
        url1 = 'https://api.elsevier.com/content/author?author_id='
        url = url1 + str(s_author_id) + "&view=ENHANCED"

        # example: https://api.elsevier.com/content/author?author_id=7005193693&apiKey=7f59af901d2d86f78a1fd60c1bf9426a&VIEW=ENHANCED

        response = requests.get(url, headers=headers)

        data = response.json()
        if not data:
            return None
        if "service-error" in data:
            return None
        searchResult = data["author-retrieval-response"]

        for k in searchResult:
            #if "coredata" in searchResult:
             #   if "document-count" in k["coredata"]:
            auth_lit.document_count = k["coredata"]["document-count"]
            auth_lit.cited_by_count = k["coredata"]["cited-by-count"]
            auth_lit.citation_count = k["coredata"]["citation-count"]
            #added in 12 Nov
            # here add the Hindex
            auth_lit.citation_all_count = k["h-index"]
            # here add the coAuthors
            auth_lit.lit_date = k["coauthor-count"]

            auth_lit.name_indexed = k["author-profile"]["preferred-name"]["indexed-name"]
            auth_lit.name_initials = k["author-profile"]["preferred-name"]["initials"]
            auth_lit.name_surname = k["author-profile"]["preferred-name"]["surname"]
            auth_lit.name_given = k["author-profile"]["preferred-name"]["given-name"]

            if "publication-range" in k["author-profile"]:
                auth_lit.start_year = k["author-profile"]["publication-range"]["@start"]
                auth_lit.end_year = k["author-profile"]["publication-range"]["@end"]
            auth_lit.save()

        return



    def IeeegetDoi(self,title_lit):

        hdr = {'Accept': 'application/json',
               "USER-AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
               }
        title_lit = "Program slicing"
        requestUrl = self.ieee_url + title_lit
        print(requestUrl)

        req = urllib.request.Request(requestUrl, headers=hdr)
        response = urllib.request.urlopen(req)
        data = json.load(response)
        if not data:
            return None

        else:
            searchResult = data["articles"]
            for u in searchResult:
                if "doi" in u:
                    doi_iee = u["doi"]
                    print(doi_iee)
                    return doi_iee

        return


    def getGender(self,  firstname,lastname):


        #conn = http.client.HTTPSConnection("v2.namsor.com", context = ssl._create_unverified_context())
        headers = {
            "content-type": "application/json",
            "X-API-KEY": "498157b630d5d44c09fe6bc8fdd8b6b4"
        }
        #params = {'author_name': s_author_name}

        url = 'https://v2.namsor.com/NamSorAPIv2/api2/json/gender/'+ firstname + "/" +lastname
        response = requests.get(url, headers=headers)
        data = response.json()
        if not data:
            return None

        return data["likelyGender"]


    def  fillauthosmissingIds_scopus(self,lit):
        if lit.doi is "":
            return
        if lit.doi is None:
            return
        else:
            doi = lit.doi
            #doi="10.1109%2FICSE.2003.1201253"
            authorsid_lis=""
            #params = {'author_id': s_author_id}
            headers = {
                'Accept': 'application/json',
                'X-ELS-APIKey': '88c15e176b1d05748dc4485439d356c6',
                'X-ELS-Insttoken': '0efaf4426dab0954258f1cb71281eeff'
            }
            url1 = 'https://api.elsevier.com/content/search/scopus?query=doi('
            url= url1+doi+")&view=COMPLETE"

            response = requests.get(url, headers=headers)

            data = response.json()
            if not data:
                return None
            if "service-error" in data:
                return None
            searchResult = data["search-results"]
            searchResult2 = searchResult["entry"]
            for u in searchResult2:
               if "author" in u:
                   for k in u["author"]:
                     authorsid_lis += k["authid"] +","
            print(authorsid_lis)
        return authorsid_lis


    def  fillauthosmissingIds_scopus_bytitle(self,lit):
        title = lit.Title
        #doi="10.1109%2FICSE.2003.1201253"
        authorsid_lis=""
        #params = {'author_id': s_author_id}
        headers = {
            'Accept': 'application/json',
            'X-ELS-APIKey': '88c15e176b1d05748dc4485439d356c6',
            'X-ELS-Insttoken': '0efaf4426dab0954258f1cb71281eeff'
        }
        url1 = 'https://api.elsevier.com/content/search/scopus?query=title('
        url= url1+title+")&view=COMPLETE"

        response = requests.get(url, headers=headers)

        data = response.json()
        if not data:
            return None
        if "service-error" in data:
            return None
        searchResult = data["search-results"]
        searchResult2 = searchResult["entry"]
        for u in searchResult2:
            if "error" in u:
                return None
            else:
                dc_title = u["dc:title"] + "."
                if title.lower() == dc_title.lower():
                    if "author" in u:
                        for k in u["author"]:
                            authorsid_lis += k["authid"] + ","
        return authorsid_lis

    def  getauthorIDfromName(self,fname,lname):
        #https://api.elsevier.com/content/search/author?query=AUTHFIRST(Edsger%20W)&AUTHLASTNAME(Dijkstra)&apiKey=88c15e176b1d05748dc4485439d356c6&Insttoken=0efaf4426dab0954258f1cb71281eeff

        authorsid_lis=""
        headers = {
            'Accept': 'application/json',
            'X-ELS-APIKey': '88c15e176b1d05748dc4485439d356c6',
            'X-ELS-Insttoken': '0efaf4426dab0954258f1cb71281eeff'
        }
        url1 = 'https://api.elsevier.com/content/search/author?query=AUTHLASTNAME('
        url2 = url1+lname+")and AUTHFIRST("
        url = url2+fname+")"

        response = requests.get(url, headers=headers)
        print(url)

        data = response.json()
        if not data:
            return None
        if "service-error" in data:
            return None
        searchResult = data["search-results"]
        searchResult2 = searchResult["entry"]
        for u in searchResult2:
            if "error" in u:
                return None
            else:
                if lname.lower() == u["preferred-name"]["surname"].lower():
                    if fname.lower() == u["preferred-name"]["given-name"].lower():
                       dc_author = u["dc:identifier"]
                       authid = dc_author.replace("AUTHOR_ID:","")
                       return authid
                if  "name-variant" in u:
                    for k in u["name-variant"]:
                        if lname.lower() == k["surname"].lower():
                           if fname.lower() == k["given-name"].lower():
                              dc_author = u["dc:identifier"]
                              authid = dc_author.replace("AUTHOR_ID:", "")
                              return authid

        return

