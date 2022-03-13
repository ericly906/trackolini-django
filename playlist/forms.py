from django import forms

class ArtistForm(forms.Form):
    artist = forms.CharField(label='artist', max_length=100)
