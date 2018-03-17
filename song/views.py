from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404
from .models import Songs, Words, Songofword
from lxml import html
import re
import requests
import logging
from bs4 import BeautifulSoup
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.

def index(request):


    return render(request,'song/index.html')

<<<<<<< HEAD
def searchindex(request):


    return render(request,'song/searchindex.html')

=======
>>>>>>> ec7d04718fd16ffeb2c751a306b1f0882c9b1dfc
def detail(request,song_id):
    try:
        document = Songs.objects.get(pk=song_id)
    except Songs.DoesNotExist:
        raise Http404("Document does not exist")

    return render(request, 'song/detail.html', {'document': document})

def view(request):
    document_list=Songs.objects.all()
    context = {'document_list': document_list}
    return render(request,'song/allsongs.html',context)

def detele_document(song_id):
    
    print ('detele_document '+  str(song_id))
    
    document = get_object_or_404(Songs, pk=song_id)
    document.delete()
<<<<<<< HEAD

=======
    
>>>>>>> ec7d04718fd16ffeb2c751a306b1f0882c9b1dfc

def wasdeleted(request):
    #import pdb; pdb.set_trace()
    doc_list=(request.POST['slected_document_ids']).split(",")
    for doc in doc_list:
        detele_document(int(doc))
    return render(request,'song/wasdeleted.html')

def create_posting_file(word_exists ,song, indexes, numbers):
    new_song_of_the_word=Songofword(word=word_exists ,song=song, times=len(indexes), indexes=numbers)
    new_song_of_the_word.save()
    return 

def song_exists(song_name):
    return Songs.objects.filter(song_name=song_name).count()>0

def get_song(song_name):
    return Songs.objects.filter(song_name=song_name)[:1].get()

def clean_text(text):
    text=text.lower()
    return text.replace('.',' ').replace('!',' ').replace(',',' ').replace('?',' ').replace('(',' ').replace(')',' ').replace('-',' ').replace('*',' ')                

def get_indexes(word,sentence):
    pattern="\\b"+word+"\\b"
    indexes = [w.start() for w in re.finditer(pattern, sentence)]
    return indexes

def create_tables(request):
    
    try:
        url=request.POST['link']
        detail=parse_url(url)
        author="Beatles"
        stop_words=['a href',]
        detail_title=detail['title']
        detail_body=detail['body']
        sentence=''
        mid=''
        if not (detail_title is None): 
                sentence= sentence+' '+clean_text(detail_title)
        else:
            s="no title"
        if not (detail_body is None):
                sentence= sentence+' '+clean_text(detail_body)
        else:
            w="no body"

        if len(sentence)>0:
            logger= logging.getLogger(__name__)
            
            numbers=''
            
            #get_song(song_name=detail_title) if 
            song=None
            if(song_exists(song_name=detail_title)):
                song=get_song(song_name=detail_title)
            else:
                song=Songs(song_name=detail_title, author_name=author, song_url=url)
                song.save()     

            for word in set(sentence.split()):
                indexes = get_indexes(word, sentence);
                #indexes = [w.start() for w in re.finditer(word, sentence)]
                for i in range(len(indexes)):
                    numbers=numbers+" "+str(indexes[i])
                
                #get or create word
                dbWord=None
                    
                if (Words.objects.filter(word=word).count()>0):
                    dbWord=Words.objects.filter(word=word)[:1].get()
                else:
                    dbWord=Words(word=word)
                    dbWord.save()
                
                #add relation word<-> dong , if not exits
                if(dbWord.songs.filter(song_name=detail_title).count()==0):
                    create_posting_file( dbWord ,song, indexes, numbers)
                
                #reset state
                numbers=''
        else:        
            error_msg="Didnt split"

        #import pdb; pdb.set_trace()

        document = get_object_or_404(Songs, id=song.id) 
        context = {'document': document}
       # warning={'error':"There is no url enetred"}
    except MultiValueDictKeyError:
        return render(request,'song/newfile.html',{'error':"There is no url enetred"})

    return render(request,'song/newfile.html',context)


def parse_url(song_url):

    page = requests.get(song_url)
    soup = BeautifulSoup(page.text, 'html.parser')
  #  tree = html.fromstring(page.content)

    author_song_name=soup.find(class_='lyric-song-head').get_text()
    body=soup.find(class_='dn').get_text()

    #title = tree.xpath('//h1[@class="firstHeading"]/text()')
   # body= tree.xpath('//div[@class="mw-parser-output"]/p[14]/text()')
    context = {
        'title': author_song_name,
        'body': body,
    }
    logger= logging.getLogger(__name__)
    logger.error(context)
    return  context

<<<<<<< HEAD


def search(request):
    filters=[]
    excludes=[]
    word_searching=[]
    search_word=request.POST['search_text']
    if search_word is "":
        raise Http404("no words found")
    terms = sentences_split(search_word)

    for term in terms:
        temp=operator_and(term)
        print(temp)
        for i in temp:
            if (i.find(" or ")==-1):
                filters.append(i)
            else:
                temp2=operator_or(i)
                for j in temp2:
                    filters.append("|"+j)        


    return render(request, 'song/result.html', {'song_list': filters})
=======
def search_by_word(request):
    try:
        song_list = Songs.objects.order_by('song_name')
        context = {
         'song_list': song_list,
        }
    except Songs.DoesNotExist:
        raise Http404("Song does not exist")
    return render(request, 'song/search.html', {'song': context})
>>>>>>> ec7d04718fd16ffeb2c751a306b1f0882c9b1dfc


def words(request):
    try:
        songwords = Songs.objects.get(pk=song_id)
    except Songs.DoesNotExist:
        raise Http404("Song does not exist")

<<<<<<< HEAD
    return render(request, 'song/words.html', {'song': songwords})

def sentences_split(wrd):
    begin_sentences=wrd.split("(")
    i=len(begin_sentences)-1
    end_sentences= begin_sentences[i].split(")")
    i-=1
    results=[]
    i2=len(end_sentences)
    j=0
    flag=1
    while(flag):
        if(j<i2):
            temp=end_sentences[j]
            print(end_sentences[j])
            j+=1
        if temp is not "" and temp is not begin_sentences[i]:
            results.append(temp)   
        if(-1<i):
            temp=begin_sentences[i]
            i-=1
        if temp is not "":
            results.append(temp)    
        if((j==i2) and (i<0)): flag=0
    return results

def operator_and(sntc):

    results=sntc.split(" and ")

    return results

def operator_or(sntc):

    results=sntc.split(" or ")

    return results    




=======
    return render(request, 'song/words.html', {'song': songwords})
>>>>>>> ec7d04718fd16ffeb2c751a306b1f0882c9b1dfc
