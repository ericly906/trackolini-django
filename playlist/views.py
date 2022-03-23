from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .graphs import *
from .models import Track, Sections, Artist
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os
from decouple import config
import requests
import base64
import json
from secrets import *

spotify_cc = SpotifyClientCredentials(client_id=config('SPOTIFY_CLIENT_ID', 'default'),
                                                           client_secret=config('SPOTIFY_CLIENT_SECRET', 'default'))
spotify = spotipy.Spotify(auth_manager=spotify_cc)
url = "https://accounts.spotify.com/api/token"
#spotify_oauth = SpotifyOAuth(client_id=config('SPOTIFY_CLIENT_ID', 'default'), client_secret=config('SPOTIFY_CLIENT_SECRET', 'default'), redirect_uri='http://localhost:8080/')

# Create your views here.
#TODO refresh tokens in the beginning of each view?
def index(request):
    return render(request, "playlist/index.html")

def home(request):
    headers = {}
    data = {}

    # Encode as Base64
    message = f"{config('SPOTIFY_CLIENT_ID', 'default')}:{config('SPOTIFY_CLIENT_SECRET', 'default')}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')

    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)
    print(r)
    #token = r.json()['access_token']

    artist_data = Artist.objects.all()
    artist_df = pd.DataFrame(list(artist_data.values()))
    artist_df = artist_df.sort_values(by='search_count', ascending=False)
    plot_div_search = gen_bar_graph_constructor(title="Most Searched Artists", x=list(artist_df['artist']), y=list(artist_df['search_count']), xlabel="Artist", ylabel="Search Count")
    response = render(request, "playlist/home.html", context={'plot_div_search': plot_div_search})
    #response['Authorization'] = "Bearer " + token
    return response

def statistics(request):
    #Only fetches top 10 tracks because it takes a while.
    #add audio_features()
    headers = {}
    data = {}

    # Encode as Base64
    message = f"{config('SPOTIFY_CLIENT_ID', 'default')}:{config('SPOTIFY_CLIENT_SECRET', 'default')}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')

    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)

    #token = r.json()['access_token']

    artist = request.GET.get('artist', '')
    if artist == '':
        return render(request, "playlist/home.html")
    search_query = spotify.search(q="artist:" + artist, type='artist')
    artist_not_found_error = "Artist not found."
    if len(search_query['artists']['items']) < 1:
        return render(request, "playlist/home.html", context={'artist_not_found_error': artist_not_found_error})
    artist = search_query['artists']['items'][0]['name']
    artist_uri = search_query['artists']['items'][0]['uri']
    artist_tracks = spotify.artist_top_tracks(artist_uri)['tracks']
    track_uris = []
    track_names = []
    for track in artist_tracks:
        track_uris.append(track['uri'])
        track_names.append(track['name'])
    track_tempos = []
    track_energy = []
    track_valence = []
    track_loudness = []
    track_key = []
    for track in track_uris:
        track_features = spotify.audio_features(track)[0]
        track_tempos.append(track_features['tempo'])
        track_energy.append(track_features['energy'])
        track_valence.append(track_features['valence'])
        track_loudness.append(track_features['loudness'])
        track_key.append(track_features['key'])
    if not Artist.objects.filter(uri=artist_uri).exists():
        new_artist = Artist(
                        uri=artist_uri,
                        artist=artist,
                        avg_tempo=sum(track_tempos)/len(track_tempos),
                        avg_energy=sum(track_energy)/len(track_energy),
                        avg_valence=sum(track_valence)/len(track_valence),
                        avg_loudness=sum(track_loudness)/len(track_loudness),
                        avg_key=sum(track_key)/len(track_key),
                        search_count=1
                        )
        new_artist.save()
    else:
        searched_artist=Artist.objects.get(uri=artist_uri)
        searched_artist.search_count += 1
        searched_artist.save()

    plot_div_tempo = bar_graph_constructor(artist, track_names, track_tempos, "Tempos (BPM)")

    plot_div_energy = bar_graph_constructor(artist, track_names, track_energy, "Energy")

    plot_div_valence = bar_graph_constructor(artist, track_names, track_valence, "Valence")

    plot_div_loudness = bar_graph_constructor(artist, track_names, track_loudness, "Loudness (LUFs)")

    plot_div_key = bar_graph_constructor(artist, track_names, track_key, "Key")

    response = render(request, "playlist/statistics.html", context={'plot_div_tempo': plot_div_tempo, 'plot_div_loudness': plot_div_loudness, 'plot_div_key': plot_div_key, 'plot_div_energy': plot_div_energy, 'plot_div_valence': plot_div_valence})
    #response['Authorization'] = "Bearer " + token
    return response



def track_analysis(request):
    headers = {}
    data = {}

    # Encode as Base64
    message = f"{config('SPOTIFY_CLIENT_ID', 'default')}:{config('SPOTIFY_CLIENT_SECRET', 'default')}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')

    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)

    #token = r.json()['access_token']

    artist = request.GET.get('artist', '')
    if artist == '':
        return render(request, "playlist/home.html")
    track = request.GET.get('track', '')
    if track == '':
        return render(request, "playlist/home.html")
    search_query = spotify.search(q="artist:" + artist + ", track:" + track, type='track')
    track_not_found_error = "Track not found."
    if len(search_query['tracks']['items']) < 1:
        return render(request, "playlist/home.html", context={'track_not_found_error': track_not_found_error})

    artist = search_query['tracks']['items'][0]['artists'][0]['name']
    #artist_uri = search_query['tracks']['items'][0]['album']['artists'][0]['uri']
    track = search_query['tracks']['items'][0]['name']
    track_uri = search_query['tracks']['items'][0]['uri']
    track_id = search_query['tracks']['items'][0]['id']
    sections = spotify.audio_analysis(track_uri)['sections']
    if not Track.objects.filter(uid=track_uri).exists():
        new_track_features = spotify.audio_features(track_uri)[0]
        new_track = Track(
                        uid=track_uri,
                        trackname=track,
                        artist=artist,
                        tempo=new_track_features['tempo'],
                        energy=new_track_features['energy'],
                        valence=new_track_features['valence'],
                        loudness=new_track_features['loudness'],
                        key=new_track_features['key'],
                        liveness=new_track_features['liveness'],
                        danceability=new_track_features['danceability'],
                        mode=new_track_features['mode'],
                        speechiness=new_track_features['speechiness'],
                        acousticness=new_track_features['acousticness'],
                        duration_ms=new_track_features['duration_ms'],
                        time_signature=new_track_features['time_signature'],
                        search_count=1
                        )
        new_track.save()
    else:
        searched_track = Track.objects.get(uid=track_uri)
        searched_track.search_count += 1
        searched_track.save()
    player = "<iframe style='border-radius:12px' src='https://open.spotify.com/embed/track/" + track_id + "' width='100%' height='380' frameBorder='0' allowfullscreen='' allow='autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture'></iframe>"

    time = []
    confidence = []
    loudness = []
    tempo = []
    tempo_confidence = []
    key = []
    key_confidence = []
    time_signature = []
    time_signature_confidence = []

    for section in sections:
        time.append(section['start'])
        confidence.append(section['confidence'])
        loudness.append(section['loudness'])
        tempo.append(section['tempo'])
        tempo_confidence.append(section['tempo_confidence'])
        key.append(section['key'])
        key_confidence.append(section['key_confidence'])
        time_signature.append(section['time_signature'])
        time_signature_confidence.append(section['time_signature_confidence'])

    plot_div_confidence = line_plot_constructor(time, confidence, "Confidence")

    plot_div_loudness = line_plot_constructor(time, loudness, "Loudness (LUFs)")

    plot_div_tempo = line_subplot_constructor(time, tempo, tempo_confidence, "Tempo", "Tempo Confidence")

    plot_div_key = line_subplot_constructor(time, key, key_confidence, "Key", "Key Confidence")

    plot_div_time_signature = line_subplot_constructor(time, time_signature, time_signature_confidence, "Time Signature", "Time Signature Confidence")

    response = render(request, "playlist/track_analysis.html", context={'artist': artist, 'track': track, 'player': player, 'plot_div_confidence': plot_div_confidence, 'plot_div_loudness': plot_div_loudness, 'plot_div_tempo': plot_div_tempo, 'plot_div_key': plot_div_key, 'plot_div_time_signature': plot_div_time_signature})
    #response['Authorization'] = "Bearer " + token
    return response
