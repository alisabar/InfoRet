from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    # ex: /song/
    path('', views.index, name='index'),

    path('newfile/', views.create_tables, name='newfile'),

    path('allsongs/', views.view, name='view'),
    
    path('wasdeleted/', views.wasdeleted, name='wasdeleted'),
    # ex: /song/5/
    path('<int:song_id>/detail/', views.detail, name='detail'),
    # ex: /song/5/words/
    path('<int:song_id>/words/', views.words, name='words'),

    path('search/', views.search, name='search'),

     path('searchindex/', views.searchindex, name='searchindex'),
]


