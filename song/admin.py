from django.contrib import admin
from .models import Songs, Words


class SongsAdmin(admin.ModelAdmin):
    fields = ['song_name', 'author_name' , 'song_url'] 
admin.site.register(Songs, SongsAdmin)



class WordsAdmin(admin.ModelAdmin):
    fields = ['song', 'word', 'times', 'indexes']  
admin.site.register(Words, WordsAdmin)