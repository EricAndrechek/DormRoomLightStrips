import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import json


def main():
    data = open('.spotify-credentials.json', 'r')
    creds = json.load(data)

    auth_manager = SpotifyOAuth(
        client_id=creds["ClientID"],
        client_secret=creds["ClientSecret"],
        redirect_uri=creds["RedirectUrl"],
        scope=creds["Scope"],
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Get the current track
    current_track = sp.current_user_playing_track()
    return current_track, sp


def get_playback_position():
    current_track, sp = main()
    if current_track is not None:
        position = current_track['progress_ms']
        return position
    else:
        return False


def get_song_duration():
    current_track, sp = main()
    if current_track is not None:
        duration = current_track['item']['duration_ms']
        return duration
    else:
        return False


def get_audio_features():
    current_track, sp = main()
    if current_track is not None:
        audio_features = sp.audio_features(current_track['item']['id'])
        return audio_features
    else:
        return False


def get_audio_analysis():
    current_track, sp = main()
    if current_track is not None:
        audio_analysis = sp.audio_analysis(current_track['item']['id'])
        return audio_analysis
    else:
        return False


if __name__ == '__main__':
    print(get_playback_position())
    print(get_audio_analysis()["beats"])
