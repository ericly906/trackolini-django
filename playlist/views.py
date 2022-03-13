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
    artist = request.GET.get('artist', '')
    artist = artist.title()
    artist_uri = spotify.search(q="artist:" + artist, type='artist')['artists']['items'][0]['uri']
    artist_tracks = spotify.artist_top_tracks(artist_uri)['tracks']
    track_uris = []
    track_names = []
    for track in artist_tracks:
        track_uris.append(track['uri'])
        track_names.append(track['name'])
    track_tempos = []
    track_loudness = []
    track_key = []
    for track in track_uris:
        track_tempos.append(spotify.audio_analysis(track)['track']['tempo'])
        track_loudness.append(spotify.audio_analysis(track)['track']['loudness'])
        track_key.append(spotify.audio_analysis(track)['track']['key'])

    fig_tempo = go.Figure()
    fig_tempo.add_trace(go.Bar(x=track_names,
                y=track_tempos, marker_color="rgb(40, 15, 107)"))
    fig_tempo.update_layout(
        title="Tempo of " + artist + " Tracks",
        xaxis_title="Track IDs",
        yaxis_title="Tempo (BPM)",
        legend_title="Legend Title",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="White"
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    plot_div_tempo = plot(fig_tempo, output_type='div', include_plotlyjs=False, show_link=False, link_text="")

    fig_loudness = go.Figure()
    fig_loudness.add_trace(go.Bar(x=track_names,
                y=track_loudness, marker_color="rgb(40, 15, 107)"))
    fig_loudness.update_layout(
        title="Loudness of " + artist + " Tracks",
        xaxis_title="Track IDs",
        yaxis_title="Loudness (LUFs)",
        legend_title="Legend Title",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="White"
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    plot_div_loudness = plot(fig_loudness, output_type='div', include_plotlyjs=False, show_link=False, link_text="")

    fig_key = go.Figure()
    fig_key.add_trace(go.Bar(x=track_names,
                y=track_key, marker_color="rgb(40, 15, 107)"))
    fig_key.update_layout(
        title="Key of " + artist + " Tracks",
        xaxis_title="Track IDs",
        yaxis_title="Key",
        legend_title="Legend Title",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="White"
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    plot_div_key = plot(fig_key, output_type='div', include_plotlyjs=False, show_link=False, link_text="")
    return render(request, "playlist/statistics.html", context={'plot_div_tempo': plot_div_tempo, 'plot_div_loudness': plot_div_loudness, 'plot_div_key': plot_div_key})
