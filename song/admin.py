from django.contrib import admin
from .models import Songs, Words ,Songofword

class SongofwordInlineAdmin(admin.TabularInline):
    model = Songofword
    #extra = 3

#class SongofwordAdmin(admin.ModelAdmin):
#    fields = ['word','song', 'times' , 'indexes']
    

#admin.site.register(Songofword, SongofwordAdmin)  

class WordsAdmin(admin.ModelAdmin):
    fields = ['word']
    inlines = (SongofwordInlineAdmin,)
admin.site.register(Words, WordsAdmin)

class SongsAdmin(admin.ModelAdmin):
    fields = ['song_name', 'author_name' , 'song_url'] 
admin.site.register(Songs, SongsAdmin)
