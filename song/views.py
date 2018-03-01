from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404
from .models import Songs, Words, WordsOfSongs

# Create your views here.

def index(request):
    song_list = Songs.objects.order_by('song_name')

    context = {
        'song_list': song_list,
    }

    return render(request,'song/index.html',context)

def detail(request,song_id):
    try:
        songdetails = Songs.objects.get(pk=song_id)
    except Songs.DoesNotExist:
        raise Http404("Song does not exist")
    return render(request, 'song/detail.html', {'song': songdetails})


def words(request):
    try:
        songwords = Songs.objects.get(pk=song_id)
    except Songs.DoesNotExist:
        raise Http404("Song does not exist")

    return render(request, 'song/words.html', {'song': songwords})