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
  

 
    return render(request,'song/detail.html',{ 'content':detail, 'songdetails':songdetails  })

def create_tables (request)
{
    url=request.POST['link']
    detail=parse_url(url)
    name=detail.title
    author=""

    content = detail.title.lower().replace('.','').replace('!','').replace(',','').replace('?','').replace('(','').replace(')','').replace('-','').replace('*','')..replace(']','').replace('[','')
    content = content + detail.body.lower().replace('.','').replace('!','').replace(',','').replace('?','').replace('(','').replace(')','').replace('-','').replace('*','')..replace(']','').replace('[','')
    content.sorted()
    for word in set(content.split()):
        indexes = [w.start() for w in re.finditer(word, content)]
        #print(word, len(indexes), indexes)
        w=Words.create(word=word, num_docs=song_id, times=len(indexes))
        s=w.songs_set.create(song_name=name, author_name=author, song_url=url)

  
    context = {
        'doc': s,
        'words': w,
    }

    return render(request,'song/newfile.html',{ 'context':contex })
}
def parse_url(song_url):
 
   # song = Songs.objects.get(pk=song_id)
   # url=song.song_url('https://en.wikipedia.org/wiki/Hayim_Nahman_Bialik')
    page = requests.get(song_url)

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