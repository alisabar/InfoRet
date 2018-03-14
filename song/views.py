from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404
from .models import Songs, Words
from lxml import html
import re
import requests
import logging
from django.utils.datastructures import MultiValueDictKeyError
# Create your views here.

def index(request):


    return render(request,'song/index.html')

def detail(request,song_id):
    songdetails = get_object_or_404(Songs, pk=song_id)

    #  songdetails = Songs.objects.get(pk=song_id)
  

 
    return render(request,'song/detail.html',{ 'content':detail, 'songdetails':songdetails  })

def create_tables(request):
    
    try:
        url=request.POST['link']
        detail=parse_url(url)
        author=""
        stop_words=['a href',]
        detail_title=detail['title']
        detail_body=detail['body']
        sentence=''
        mid=''
        if not (detail_title is None):
            for x in range(len(detail_title)):
                mid=detail_title[x]
                mid=mid.lower()
                mid= mid.replace('.','').replace('!','').replace(',','').replace('?','').replace('(','').replace(')','').replace('-','').replace('*','')
                sentence= sentence+' '+mid

        else:
            s="no title"

        if not (detail_body is None):
        
            for x in range(len(detail_body)):
                mid=detail_body[x]
                mid= mid.lower()
                mid= mid.replace('.','').replace('!','').replace(',','').replace('?','').replace('(','').replace(')','').replace('-','').replace('*','')
                sentence= sentence+' '+mid
        else:
            w="no body"

        if len(sentence)>0:
            numbers=''
            s=Songs(song_name=detail_title, author_name=author, song_url=url)
            s.save()
            for word in set(sentence.split()):

                indexes = [w.start() for w in re.finditer(word, sentence)]
                for i in range(len(indexes)):
                    numbers=numbers+" "+str(indexes[i])

                w=Words(song=s, word=word, times=len(indexes), indexes=numbers)
                w.save(force_insert=True)
                s.words_set.add(w)
                
                s.save()
                numbers=''
        else:        
            error_msg="Didnt split"

        document = get_object_or_404(Songs, id=s.id) 
        context = {'document': document}
        warning={'error':"There is no url enetred"}
    except MultiValueDictKeyError:
        return render(request,'song/newfile.html',warning)

    return render(request,'song/newfile.html',context)

def parse_url(song_url):
 
   # song = Songs.objects.get(pk=song_id)
   # url=song.song_url('https://en.wikipedia.org/wiki/Hayim_Nahman_Bialik')
    page = requests.get(song_url)

    tree = html.fromstring(page.content)

    title = tree.xpath('//h1[@class="firstHeading"]/text()')
    body= tree.xpath('//div[@class="mw-parser-output"]/p[14]/text()')
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