import logging
from urllib.parse import urlparse
from pathlib import Path
import datetime
from os import getenv as env

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

from dotenv import load_dotenv

from spotify_stats import TrackDetails

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CLIENT_ID = env('CLIENT_ID')
CLIENT_SECRET = env('CLIENT_SECRET')

CREDENTIALS_MANAGER = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
SPOTIFY_CLIENT = None

def get_spotify_client():
    global SPOTIFY_CLIENT
    if SPOTIFY_CLIENT is None:
        SPOTIFY_CLIENT = spotipy.Spotify(client_credentials_manager=CREDENTIALS_MANAGER)
    return SPOTIFY_CLIENT

def playlist_url_to_id(url):
    """
    https://open.spotify.com/playlist/5zo4GGZoBqnA8VWE7Mf3Ve?trackingstuff=1234
    => spotify:playlist:5zo4GGZoBqnA8VWE7Mf3Ve
    """
    logger.debug("Getting playlist id from url {}".format(url))
    playlist_id = Path(urlparse(url).path).name
    logger.debug("Url {} converted to id {}".format(url, playlist_id))
    return playlist_id

def playlist_id_to_track_list(playlist_id):
    logger.debug("Getting tracks for {}".format(playlist_id))
    start_time = datetime.datetime.now()
    spotify = get_spotify_client()
    spotify_fields = 'items.track.id,total'

    offset = 0
    items = []
    while True:
        urn = "spotify:playlist:" + playlist_id
        response = spotify.playlist_tracks(urn, offset=offset, fields=spotify_fields)
        total = response['total']
        response_items = [track['track']['id'] for track in response['items']]
        if len(response_items) == 0:
            break
        items.extend(response_items)
        offset = offset + len(response_items)
        logger.debug("Received playlist tracks {}/{}".format(offset, total))
    seconds = (datetime.datetime.now() - start_time).total_seconds()
    logger.debug("{} took {} seconds to run, with results {}".format(playlist_id_to_track_list.__name__, seconds, items))
    return items

def track_list_to_details(track_list):
    urns = ["spotify:track:" + track for track in track_list]
    logger.debug("Getting track details for {}".format(track_list))
    spotify = get_spotify_client()
    start_time = datetime.datetime.now()
    details = []
    while len(urns) > 0:
        urns_chunk = urns[0:50]
        urns = urns[50:]
        tracks = spotify.tracks(urns_chunk)['tracks']
        features = spotify.audio_features(urns_chunk)
        for info in zip(tracks, features):
            track = TrackDetails()
            track.title = info[0]['name']
            track.artist = info[0]['artists'][0]['name']
            track.duration = info[0]['duration_ms'] / 1000
            track.danceability = info[1]['danceability']
            track.energy = info[1]['energy']
            track.loudness = info[1]['loudness']
            track.speechiness = info[1]['speechiness']
            track.instrumentalness = info[1]['instrumentalness']
            track.valence = info[1]['valence']
            track.tempo = info[1]['tempo']
            track.time_signature = info[1]['time_signature']
            track.key = info[1]['key']
            details.append(track)
    seconds = (datetime.datetime.now() - start_time).total_seconds()
    logger.debug("{} took {} seconds to run, with results {}".format(track_list_to_details.__name__, seconds, details))
    return details
