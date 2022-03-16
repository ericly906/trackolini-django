from django.db import models

# Create your models here.
class Track(models.Model):
    uid = models.CharField(max_length=255)
    trackname = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    tempo = models.IntegerField()
    energy = models.IntegerField()
    valence = models.IntegerField()
    loudness = models.IntegerField()
    key = models.IntegerField()
    liveness = models.IntegerField()
    danceability = models.IntegerField()
    mode = models.IntegerField()
    speechiness = models.IntegerField()
    acousticness = models.IntegerField()
    duration_ms = models.IntegerField()
    time_signature = models.IntegerField()
    search_count = models.IntegerField(default=0)

class Sections(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    start = models.IntegerField()
    duration = models.IntegerField()
    confidence = models.IntegerField()
    loudness = models.IntegerField()
    tempo = models.IntegerField()
    tempo_confidence = models.IntegerField()
    key = models.IntegerField()
    key_confidence = models.IntegerField()
    mode = models.IntegerField()
    mode_confidence = models.IntegerField()
    time_signature = models.IntegerField()
    time_signature_confidence = models.IntegerField()
    
