from django.db import models

# Create your models here.
class Song(models.Model):
    song_name= models.CharField(max_length=300)
    author_name= models.CharField(max_length=300)
    
    def __str__(self):
        return ' song_name: %s , author_name: %s \n' % (self.song_name, self.author_name)

class Songwords(models.Model):
    song=models.ForeignKey(Song, on_delete=models.CASCADE)
    song_words= models.CharField(max_length=10000)
    def __str__(self):
        return ' song: %s , song words: %s \n' % (self.song,  self.song_words)

class Word(models.Model): 
    song=models.ForeignKey(Songwords, on_delete=models.CASCADE) 
    word=models.CharField(max_length=100)
    def __str__(self):
        return ' word: %s, song: %s \n' % (self.word, self.song)


    