from django.contrib import admin
from .models import Songs, Words , Songofword


class SongsAdmin(admin.ModelAdmin):
    fields = ['song_name', 'author_name' , 'song_url'] 
admin.site.register(Songs, SongsAdmin)

class SongofwordAdmin(admin.ModelAdmin):
    fields = ['song', 'times' , 'indexes'] 
admin.site.register(Songofword, SongofwordAdmin)  

class WordsAdmin(admin.ModelAdmin):
    fields = ['songs','word']  
admin.site.register(Words, WordsAdmin)

