from django.contrib import admin
from .models import Songs, Words, WordsOfSongs

admin.site.register(Songs)
admin.site.register(Words)
admin.site.register(WordsOfSongs)
# Register your models here.
