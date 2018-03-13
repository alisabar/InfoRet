from django.db import models

# Create your models here.

class Songs(models.Model):
    song_name= models.CharField(max_length=300)
    author_name= models.CharField(max_length=300)
    song_url= models.CharField(max_length=10000)
    def __str__(self):
        return ' song_name: %s , author_name: %s ,song_url: %s \n' % (  self.song_name, self.author_name, self.song_url)


class Words(models.Model): 
    song= models.ForeignKey(Songs, on_delete=models.CASCADE)
    word=models.CharField(max_length=100)
    times=models.IntegerField(default=0)
    indexes=models.CharField(max_length=100)
    def __str__(self):
        return 'song: %s, word: %s, times: %d , indexes: %s \n' % (self.song, self.word, self.times, self.indexes)


    