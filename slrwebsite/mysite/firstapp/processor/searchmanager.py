from ..models.literatureCl import LiteratureCl
from ..models.reverseIndexItem import ReverseIndexItem, WordType

from django.db import connection
import pandas as pd
import sqlite3



import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


class SearchManager:

    @staticmethod
    def searchinReverseIndex(keyword, textype):
        reveitemlist_lit = ReverseIndexItem.objects.filter(word__exact=keyword).filter(type__exact=textype)
        return reveitemlist_lit

    @staticmethod
    def searchinLitAuther(author):
        literatur_authers = LiteratureCl.objects.filter(word__exact=author)
        return literatur_authers

    @staticmethod
    def searchByKeywordsLogicalOperation(keywords):
        if not keywords:
            return
        sqlStmt = '''Select T3.word, SUM(T3.COUNT) , T3.literature_id  FROM 
        (SELECT T2.word, T2.count, T2.literature_id, T2.type
        FROM firstapp_reverseindexitem T2 
        WHERE T2.literature_id IN ('''
        innerSqlStmtTemplate = '''SELECT T1.literature_id FROM firstapp_reverseindexitem T1
            WHERE T1.word in '''
        innerSqlStmt = ''
        allKeyWords = ''
        for keyword in keywords:
            list = keyword.split(',')
            innerKeywords = ''
            for orKeyword in list:
                allKeyWords = allKeyWords + '\''+orKeyword.strip()+'\','
                innerKeywords = innerKeywords + '\''+orKeyword.strip()+'\','
            innerKeywords = innerKeywords[:-1]

            innerSqlStmt = innerSqlStmt + innerSqlStmtTemplate + '(' + innerKeywords + ') INTERSECT'
            innerSqlStmt = innerSqlStmt + ' '
        innerSqlStmt = innerSqlStmt[:-10]
        allKeyWords = allKeyWords[:-1]
        sqlStmt = sqlStmt + innerSqlStmt + ') AND T2.word in (' + allKeyWords + ') '
        sqlStmt = sqlStmt + 'ORDER BY literature_id) T3 GROUP BY T3.word, T3.literature_id ORDER BY literature_id'

        sqlStmt2 = 'Select * FROM firstapp_literaturecl T3'
        print(sqlStmt)
        cursor = connection.cursor()
        cursor.execute(sqlStmt)
        return cursor.fetchall()

    @staticmethod
    def myselect():
        cursor = connection.cursor()
        Lit_all_list = LiteratureCl.objects.filter(AuthorsID="")
        for litrec in Lit_all_list:
            title = litrec.Title
            sql = "UPDATE firstapp_literaturecl SET AuthorsID = (SELECT AuthorsID FROM ExtractedicseData e " \
                  "WHERE e.title= '%s') where AuthorsID="" ;"
            print(sql)
            cursor.execute(sql % (title))
            connection.commit()

        return




