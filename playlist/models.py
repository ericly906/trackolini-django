from django.db import models
#TODO: change some fields to floats
# Create your models here.
class Track(models.Model):
    uid = models.CharField(max_length=255)
    trackname = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    tempo = models.FloatField()
    energy = models.FloatField()
    valence = models.FloatField()
    loudness = models.FloatField()
    key = models.FloatField()
    liveness = models.FloatField()
    danceability = models.FloatField()
    mode = models.FloatField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    duration_ms = models.FloatField()
    time_signature = models.FloatField()
    search_count = models.IntegerField(default=0)
    def __str__(self):
        return self.trackname + ' by ' + self.artist

class Sections(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    start = models.FloatField()
    duration = models.FloatField()
    confidence = models.FloatField()
    loudness = models.FloatField()
    tempo = models.FloatField()
    tempo_confidence = models.FloatField()
    key = models.FloatField()
    key_confidence = models.FloatField()
    mode = models.FloatField()
    mode_confidence = models.FloatField()
    time_signature = models.FloatField()
    time_signature_confidence = models.FloatField()
    def __str__(self):
        return self.trackname + ' by ' + self.artist

class Artist(models.Model):
    uri = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    avg_tempo = models.FloatField()
    avg_energy = models.FloatField()
    avg_valence = models.FloatField()
    avg_loudness = models.FloatField()
    avg_key = models.FloatField()
    search_count = models.IntegerField()
    def __str__(self):
        return self.artist
