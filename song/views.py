from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404
from .models import Song, Songwords, Word

# Create your views here.

def index(request):
    song_list = Song.objects.order_by('song_name')

    context = {
        'song_list': song_list,
    }

    return render(request,'song/index.html',context)

def detail(request,song_id):
    try:
        songdetails = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        raise Http404("Song does not exist")
    return render(request, 'song/detail.html', {'song': songdetails})


def words(request):
    try:
        songwords = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        raise Http404("Song does not exist")

    return render(request, 'song/words.html', {'song': songwords})