from django.db import models

# Create your models here.
class Songs(models.Model):
    song_name= models.CharField(max_length=300)
    author_name= models.CharField(max_length=300)
    song_url= models.CharField(max_length=10000)
    def __str__(self):
        return ' song_name: %s , author_name: %s ,song_url: %s \n' % (self.song_name, self.author_name, self.song_url)

class Words(models.Model): 
    word=models.CharField(max_length=100)
    num_docs=models.IntegerField()

    def __str__(self):
        return ' word: %s, num_docs: %s \n' % (self.word, self.num_docs)

class WordsOfSongs(models.Model):
    words= models.ForeignKey(Words, on_delete=models.CASCADE)
    songs= models.ForeignKey(Songs, on_delete=models.CASCADE)
    num_songs= models.IntegerField()
    def __str__(self):
        return ' words: %s , songs: %s, num_songs: %s \n' % (self.words,  self.songs, self.num_songs)




    