from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404
from .models import Songs, Words, WordsOfSongs
from lxml import html
import requests
import logging
# Create your views here.

def index(request):

    song_list = Songs.objects.order_by('song_name')

    context = {
        'song_list': song_list,
    }

    return render(request,'song/index.html',context)

def detail(request,song_id):
    songdetails = get_object_or_404(Songs, pk=song_id)
    #  songdetails = Songs.objects.get(pk=song_id)
    detail=parse_url(songdetails)

    return render(request,'song/detail.html',{ 'content':detail, 'songdetails':songdetails  })

def parse_url(songdetails):
 
   # song = Songs.objects.get(pk=song_id)
   # url=song.song_url('https://en.wikipedia.org/wiki/Hayim_Nahman_Bialik')
    page = requests.get(songdetails.song_url)

    tree = html.fromstring(page.content)

    title = tree.xpath('//h1[@class="firstHeading"]/text()')
    body= tree.xpath('//div[@class="mw-parser-output"]/p/text()')
    context = {
        'title': title,
        'body': body,
    }
    logger= logging.getLogger(__name__)
    logger.error(context)
    return  context

def search_by_word(request):
    try:
        song_list = Songs.objects.order_by('song_name')
        context = {
         'song_list': song_list,
        }
    except Songs.DoesNotExist:
        raise Http404("Song does not exist")
    return render(request, 'song/search.html', {'song': context})


def words(request):
    try:
        songwords = Songs.objects.get(pk=song_id)
    except Songs.DoesNotExist:
        raise Http404("Song does not exist")

    return render(request, 'song/words.html', {'song': songwords})