
#from django.conf.urls import re_path
from django.urls import include, path, re_path
from django.urls import reverse



from . import views

urlpatterns = [
   # path('', views.index, name='index')
    re_path('index',views.index, name='index'),
    re_path('listkw', views.listkw, name='list'),
    re_path('startProcess', views.startProcess, name='startProcess'),
    re_path('bibpage', views.bibpage, name='bibpage'),
    re_path('contentsearch', views.contentsearch, name='contentsearch'),
    re_path('searchByAuthor', views.searchByAuthor, name='searchByAuthor'),
    re_path('search', views.search, name='search'),
    re_path('tryonly', views.tryonly, name='tryonly'),
    re_path('chartspearman', views.chartspearman, name='chartspearman'),
    re_path('chart', views.chart, name='chart'),
    re_path('quality_scoring', views.quality_scoring, name='quality_scoring'),
    re_path('amona', views.amona, name='amona'),

]
