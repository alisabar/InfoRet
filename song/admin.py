from django.contrib import admin
from .models import Songs, Words, WordsOfSongs

#admin.site.register(Songs)
#admin.site.register(Words)
#admin.site.register(WordsOfSongs)
# Register your models here.
class SongsAdmin(admin.ModelAdmin):
    fields = ['song_name', 'author_name' , 'song_url']
admin.site.register(Songs, SongsAdmin)

class WordsOfSongsAdmin(admin.ModelAdmin):
    fields = ['words', 'songs' , 'num_songs']
admin.site.register(WordsOfSongs, WordsOfSongsAdmin)

class WordsAdmin(admin.ModelAdmin):
    fields = ['word', 'num_docs'] 
admin.site.register(Words, WordsAdmin)