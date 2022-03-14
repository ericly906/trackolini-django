from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import ArtistForm

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="ccd3e124a27a4369873ad631f0e7bc21",
                                                           client_secret="c2dd204ea9d14b2faa3cfbc3bc80abcf"))

# Create your views here.
def index(request):
    return render(request, "playlist/index.html")

def home(request):
    return render(request, "playlist/home.html")

def statistics(request):
    #Only fetches top 10 tracks because it takes a while.
    #add audio_features()
    artist = request.GET.get('artist', '')
    if artist == '':
        return render(request, "playlist/home.html")
    artist = spotify.search(q="artist:" + artist, type='artist')['artists']['items'][0]['name']
    artist_uri = spotify.search(q="artist:" + artist, type='artist')['artists']['items'][0]['uri']
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

    plot_div_tempo = bar_graph_constructor(artist, track_names, track_tempos, "Tempos (BPM)")

    plot_div_energy = bar_graph_constructor(artist, track_names, track_energy, "Energy")

    plot_div_valence = bar_graph_constructor(artist, track_names, track_valence, "Valence")

    plot_div_loudness = bar_graph_constructor(artist, track_names, track_loudness, "Loudness (LUFs)")

    plot_div_key = bar_graph_constructor(artist, track_names, track_key, "Key")

    return render(request, "playlist/statistics.html", context={'plot_div_tempo': plot_div_tempo, 'plot_div_loudness': plot_div_loudness, 'plot_div_key': plot_div_key, 'plot_div_energy': plot_div_energy, 'plot_div_valence': plot_div_valence})

def bar_graph_constructor(artist, tracks, feature, label):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=tracks, y=feature, marker_color="rgb(40, 15, 107)"))
    fig.update_layout(
        title=label + " of " + artist + " Tracks",
        xaxis_title="Tracks",
        yaxis_title=label,
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="White"
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_showticklabels=False
    )
    return plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")

def track_analysis(request):
    artist = request.GET.get('artist', '')
    if artist == '':
        return render(request, "playlist/home.html")
    track = request.GET.get('track', '')
    if track == '':
        return render(request, "playlist/home.html")
    search_query = spotify.search(q="artist:" + artist + ", track:" + track, type='track')
    artist = search_query['tracks']['items'][0]['artists'][0]['name']
    track = search_query['tracks']['items'][0]['name']
    track_uri = search_query['tracks']['items'][0]['uri']
    section_analysis = spotify.audio_analysis(track_uri)['sections']

    
    return render(request, "playlist/track_analysis.html")
