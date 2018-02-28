from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    # ex: /song/
    path('', views.index, name='index'),
    # ex: /song/5/
    path('<int:song_id>/', views.detail, name='detail'),
    # ex: /song/5/words/
    path('<int:song_id>/words/', views.words, name='words'),

]


