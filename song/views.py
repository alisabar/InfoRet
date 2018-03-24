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
important_words=[]

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

def wildcard(request):
    str=request.POST['word']
    print(str)
    #documents= Songs.objects.filter(songofword__word__word__regex=r'str.*')
    documents=Words.objects.filter(word='is')
    print(documents)
    return render(request, 'song/regex.html', {'documents': documents})

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
    new_song_of_the_word=Songofword(word=word_exists ,song=song, times=indexes, indexes=numbers)
    new_song_of_the_word.save()
    return 

def song_exists(song_name):
    return Songs.objects.filter(song_name=song_name).count()>0

def get_song(song_name):
    return Songs.objects.filter(song_name=song_name)[:1].get()

def scontent(request,song_id,search_words):
    try:
        song = Songs.objects.get(pk=song_id)
    except Songs.DoesNotExist:
        raise Http404("Document does not exist")
    context={
        'song': song,
        'words':search_words,
    }
    return render(request, 'song/scontent.html', context)

def clean_text(text):

    body=str(text)
    body= body.replace('a href',' ').replace('<div class="dn" id="content_h">',' ').replace('<br/>',' ').replace('</div>',' ')
    body=body.lower()
    return body.replace('.',' ').replace('!',' ').replace(',',' ').replace('?',' ').replace('(',' ').replace(')',' ').replace('-',' ').replace('*',' ').replace('–',' ').replace('[',' ').replace(']',' ').replace('\"',' ').replace('\'ll',' will ').replace('\'s',' ').replace('\'d',' would ').replace("'cause","because")      

def create_index_array(sentence):
    indexes=[]
    words=sentence.split()
    for i in range(0,len(words)):
        indexes.append(words[i]);
    return indexes

def create_dict_index(indexes):

    list_dict={}
    for i in range(0,len(indexes)):
        if indexes[i] not in list_dict:
            list_dict[indexes[i]]=[i]
        else:
            list_dict[indexes[i]].append(i)
    return list_dict


def get_indexes(word,sentence):
    pattern="\\b"+word+"\\b"

    indexes=[]
    for word in sentence:


        indexes = [w.start() for w in re.finditer(pattern, sentence)]

    return indexes

def create_tables(request):
    
    try:
        url=request.POST['link']
        detail=parse_url(url)
       
       
        detail_title=detail['title']
        detail_body=detail['body']
        author=''
        name=''
        sentence=''
        mid=''
        content_song_lyrics=detail['song_content']
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
                if not(content_song_lyrics is None):
                    song=Songs(song_content=content_song_lyrics, song_name=name, author_name=author, song_url=url)
                    song.save()  
                else:
                    p="no context"   
            index_array=create_index_array(content_song_lyrics)
            how_many_times_a_word_repeats=create_dict_index(index_array)

            content_song_lyrics=str(content_song_lyrics)
            for word in index_array:

                #indexes = get_indexes(word, content_song_lyrics);


                #indexes = [w.start() for w in re.finditer(word, sentence)]
               # for i in range(len(indexes)):
                  #  numbers=numbers+" "+str(indexes[i])
                
                #get or create word
                dbWord=None
                    
                if (Words.objects.filter(word=word).count()>0):
                    dbWord=Words.objects.filter(word=word)[:1].get()
                else:
                    dbWord=Words(word=word)
                    dbWord.save()
                
                #add relation word<-> dong , if not exits
                if(dbWord.songs.filter(song_name=name).count()==0):

                    create_posting_file( dbWord ,song, len(how_many_times_a_word_repeats[word]), how_many_times_a_word_repeats[word])
                    indexes=0
                

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

    song_content=str(body)
    song_content= song_content.replace('<div class="dn" id="content_h">',' ').replace('</div>',' ').replace('<br/>',' <br>')
    song_content=clean_text(song_content)
        
    #title = tree.xpath('//h1[@class="firstHeading"]/text()')
   # body= tree.xpath('//div[@class="mw-parser-output"]/p[14]/text()')
    context = {
        'title': author_song_name,
        'body': body,
        'song_content':song_content,
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
    search_words=[]
    stop_words=['the', 'they', 'is', 'are']
    ids=[]
    search_word=request.POST['search_text']
    for i in stop_words:
        search_word=search_word.replace(i,'')
    if search_word is "":
        raise Http404("no words found")
    print(search_word)
    terms = sentences_split(search_word)

    words=terms[0].split()
    
    if(len(words)==1):
        if '*' not in words[0]:
            search_words.append(words[0])
            results=Songs.objects.filter(is_searchable=1).filter(songofword__word__word=words[0]).order_by('-songofword__times')
        else:
            words[0]=wildcard(words[0])
            search_words.append(words[0])
            results=Songs.objects.filter(is_searchable=1).filter(songofword__word__word__contains=words[0]).order_by('-songofword__times')
    else:
        if (words[1].find("and")!=-1):
            search_words.append(words[0])
            search_words.append(words[2])
            results=Songs.objects.filter(is_searchable=1).filter(songofword__word__word=words[0]).filter(songofword__word__word=words[2]).order_by('-songofword__times')
        elif (words[1].find("or")!=-1):
            search_words.append(words[0])
            search_words.append(words[2])
            results=Songs.objects.filter(is_searchable=1).filter(Q(songofword__word__word=words[0])|Q(songofword__word__word=words[2])).order_by('-songofword__times')
        elif (words[1].find("near")!=-1):
            search_words.append(words[0])
            search_words.append(words[3])
            results= near(words[0],words[3],int(words[2]))


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
                    search_words.append(words[1])
                    results=operator_and(ids,words[1])
                else:
                    search_words.append(words[0])
                    results=operator_and(ids,words[0])
                temp=[]
                for j in results:
                    temp.append(j.id)
                ids=temp            
            elif "or" in words:
                if (words[0]=="or"):
                    search_words.append(words[1])
                    results=operator_or(ids,words[1])
                else:
                    search_words.append(words[0])
                    results=operator_or(ids,words[0])
            for j in results:
                if j.id not in ids:
                    print(j.id)
                    ids.append(j.id)              
            i+=1

    for i in ids:
        songlist.append(Songs.objects.get(id=i))

    important_words=search_words


    str1 = ','.join(str(e) for e in words)
    context={
        'song_list': songlist,
        'search_words': str1,
    }



    return render(request, 'song/result.html', context)



#def find_distance(word1,word2, min_dist):
    
#    word_1 = get_object_or_404(Words, word=word1)
#    word_1_indexes=word_1.songs.indexes
#    word_2 = get_object_or_404(Words, word=word2)
#    word_2_indexes=word_2.songs.indexes
#    dist=min_dist
#    mindist=100
 
 #   distenses=[]
  #  for i in word_1_indexes:
   #     for j in word_2_indexes:
    #        if abs(i-j)>dist:
     #           continue
      #      else
       #         dist=abs(i-j)
        #        y={'i'=i, 'j'=j, 'distanse'=dist}
         #       distenses.apend(y)
                                
                
  #  return distenses

#def extract_distance(distenses):

 #     dict_of_distanses=distenses 
      


#def bold(song, word){
 #   song_obj=song
  #  song_text=song_obj.song_content
   # song_new_text=f(song_text)
    
#}                
#def f(song_text):
 #   str=



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
               
def make_word_bold(song_text, words):

    str_song=song_text.split()
    for j in words:
        for i in str_song:
            if str_song[i]==word:
                m=str_song[i]
                str_song[i]='<b>'+m+'</b>'
    return str_song


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
        results=Songs.objects.filter(is_searchable=1).filter(songofword__word__word=word).filter(id__in=ids).order_by('-songofword__times')
    else:
        word=wildcard(word)
        results=Songs.objects.filter(is_searchable=1).filter(songofword__word__word__contains=word).filter(id__in=ids).distinct().order_by('-songofword__times')
    return results

def operator_or(ids,word):
    if '*' not in word:
        results=Songs.objects.filter(is_searchable=1).filter(Q(songofword__word__word=word)|Q(id__in=ids)).order_by('-songofword__times')
    else:
        word=wildcard(word)
        results=Songs.objects.filter(is_searchable=1).filter(Q(songofword__word__word__contains=word)|Q(id__in=ids)).order_by('-songofword__times')
        print(Words.objects.filter(word__contains=word))
    return results    

def wildcard(word):
    print(word)
    result=word.split('*')[0]
    return result

def near(word1,word2,dis):
  
  results1=Songs.objects.filter(is_searchable=1).filter(songofword__word__word=word1).filter(songofword__word__word=word2)
  ids=[]
  for i in results1:
        indexes1=Songofword.objects.filter(song=i).filter(word__word=word1)
        indexes1=indexes1[0].indexes.split()
        indexes2=Songofword.objects.filter(song=i).filter(word__word=word2)
        indexes2=indexes2[0].indexes.split()
        for i1 in indexes1:
            for i2 in indexes2:
                dis1=int(i1)
                dis2=int(i2)
                if(dis>=abs(dis1-dis2)):
                    ids.append(i.id)

  results=Songs.objects.filter(id__in=ids) 
  print(results)
  return results                 
