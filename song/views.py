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
from django.db.models import Q

# Create your views here.

def index(request):


    return render(request,'song/index.html')

def searchindex(request):

    return render(request,'song/searchindex.html')

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

def delete_song(song_id):

    song_to_delete=get_object_or_404(Songs, id=song_id)
    song_to_delete.is_searchable=0
    song_to_delete.save() 

def delete_word(word_id):

    word_to_delete=get_object_or_404(Words, id=word_id)
    word_to_delete.is_searchable=0
    word_to_delete.save()

def songwasdeleted(request):
    #import pdb; pdb.set_trace()
    doc_list=(request.POST['slected_document_ids']).split(",")
    for doc in doc_list:
        delete_song(int(doc))
    return render(request,'song/wasdeleted.html')

def wordwasdeleted(request):
    #import pdb; pdb.set_trace()
    doc_list=(request.POST['slected_document_ids']).split(",")
    for doc in doc_list:
        detele_word(int(doc))
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

    body=str(text)
    body= body.replace('<div class="dn" id="content_h">',' ').replace('<br/>',' ').replace('</div>',' ')
    body=body.lower()

    return body.replace('.',' ').replace('!',' ').replace(',',' ').replace('?',' ').replace('(',' ').replace(')',' ').replace('-',' ').replace('*',' ').replace('–',' ').replace('[',' ').replace(']',' ').replace('\"',' ').replace('\'ll',' will ').replace('\'s',' ').replace('\'d',' would ').replace("'cause","because")      

def get_indexes(word,sentence):
    pattern="\\b"+word+"\\b"
    indexes = [w.start() for w in re.finditer(pattern, sentence)]
    return indexes

def create_tables(request):
    
    try:
        url=request.POST['link']
        detail=parse_url(url)
       
        stop_words=['a href',]
        detail_title=detail['title']
        detail_body=detail['body']
        author=''
        name=''
        sentence=''
        mid=''
        if not (detail_title is None): 
                author = detail_title.split("–")[0]
                name=detail_title.split("–")[1:]
                name=str(name)
                name=name.replace('[',' ').replace(']',' ').replace("'",' ').replace('Lyrics',' ')
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
            if(song_exists(song_name=name)):
                song=get_song(song_name=name)
            else:
                song=Songs(song_name=name, author_name=author, song_url=url)
                song.save()     

          #  import pdb; pdb.set_trace()
            sorted_sentence=sorted(sentence.split())
            for word in set(sorted_sentence):
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
                if(dbWord.songs.filter(song_name=name).count()==0):
                    create_posting_file( dbWord ,song, indexes, numbers)
                
                #reset state
                numbers=''
        else:        
            error_msg="Didnt split"

        #import pdb; pdb.set_trace()

        document = get_object_or_404(Songs, id=song.id) 

        #document.songofword_set.word.objects.order_by('word')
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
    body=soup.find(class_='dn')

    #title = tree.xpath('//h1[@class="firstHeading"]/text()')
   # body= tree.xpath('//div[@class="mw-parser-output"]/p[14]/text()')
    context = {
        'title': author_song_name,
        'body': body,
    }
    logger= logging.getLogger(__name__)
    logger.error(context)
    return  context

def search(request):
    
    filters=[]
    excludes=[]
    words=[]
    ands=[]
    ors=[]
    songlist=[]
    results=[]  
    
    ids=[]
    search_word=request.POST['search_text']
    if search_word is "":
        raise Http404("no words found")
    terms = sentences_split(search_word)

    words=terms[0].split()

    if(len(words)==1):
        if '*' not in words[0]:
            results=Songs.objects.filter(is_searchable=1).filter(songofword__word__word=words[0]).order_by('songofword__times')
        else:
            words[0]=wildcard(words[0])
            results=Songs.objects.filter(is_searchable=1).filter(songofword__word__word__contains=words[0])
    else:
        if (words[1].find("and")!=-1):
            results=Songs.objects.filter(is_searchable=1).filter(songofword__word__word=words[0]).filter(songofword__word__word=words[2])
        elif (words[1].find("or")!=-1):
            results=Songs.objects.filter(is_searchable=1).filter(Q(songofword__word__word=words[0])|Q(songofword__word__word=words[2]))
    
    for i in results:
        if i.id not in ids:
            print(i.id)
            ids.append(i.id)

    if(len(terms)>1):
        i=1
        while i<len(terms):
            words=terms[i].split()
            if "and" in words:
                if (words[0]=="and"):
                    results=operator_and(ids,words[1])
                else:
                    results=operator_and(ids,words[0])
                temp=[]
                for j in results:
                    temp.append(j.id)
                ids=temp            
            elif "or" in words:
                if (words[0]=="or"):
                    results=operator_or(ids,words[1])
                else:
                    results=operator_or(ids,words[0])
            for j in results:
                if j.id not in ids:
                    print(j.id)
                    ids.append(j.id)              
            i+=1

    for i in ids:
        songlist.append(Songs.objects.get(id=i))
   
    

    return render(request, 'song/result.html', {'song_list': songlist})


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

def operator_and(ids,word):
    if '*' not in word:
        results=Songs.objects.filter(is_searchable=1).filter(songofword__word__word=word).filter(id__in=ids)
    else:
        word=wildcard(word)
        results=Songs.objects.filter(is_searchable=1).filter(songofword__word__word__contains=word).filter(id__in=ids).distinct()
    return results

def operator_or(ids,word):
    if '*' not in word:
        results=Songs.objects.filter(is_searchable=1).filter(Q(songofword__word__word=word)|Q(id__in=ids))
    else:
        word=wildcard(word)
        results=Songs.objects.filter(is_searchable=1).filter(Q(songofword__word__word__contains=word)|Q(id__in=ids))
        print(Words.objects.filter(word__contains=word))
    return results    

def wildcard(word):
    print(word)
    result=word.split('*')[0]
    return result