import configparser

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def search(types, type_name, limit):
    def my_search_decorator(func):
        def wrapped(self, name):
            result_search = []
            for self.i in self.spotify.search(q=name, type=types, limit=limit)[type_name]['items']:
                result_search.append(func(self))
            return result_search
        return wrapped
    return my_search_decorator


class SpotifySearch:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('setting.ini')

        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=config.get('Spotify', 'client_id'), client_secret=config.get('Spotify','client_secret')))

    def _get_image(self, obj):
        if obj['images'] != []:
            return obj['images'][0]["url"]
        else:
            return None

    @search(types="artist", type_name="artists", limit=35)
    def search_artist(self):
        return {"artist_name": self.i["name"],
                "images": self._get_image(self.i),
                "url": self.i['external_urls']['spotify']}

    @search(types="album", type_name="albums", limit=15)
    def search_album(self):
        return {"artist": self.i['artists'][0]['name'],
                "artist_url": self.i['artists'][0]["external_urls"]["spotify"],
                "album": self.i['name'],
                "images": self._get_image(self.i),
                "url": self.i['external_urls']['spotify']}

    @search(types="track", type_name="tracks", limit=50)
    def search_track(self):
        return {'artist': self.i['artists'][0]['name'],
                'artist_url': self.i['artists'][0]["external_urls"]["spotify"],
                'track': self.i['name'],
                "images": self._get_image(self.i["album"]),
                "url": self.i["external_urls"]["spotify"],
                "album_url": self.i["album"]["external_urls"]["spotify"],
                "album_name": self.i["album"]["name"]}

    def artist_info(self, url):
        artist = self.spotify.artist(artist_id=url)
        return {
            'name': artist['name'],
            'image': self._get_image(artist)
        }

    def get_list_album(self, uri):
        albums = self.spotify.artist_albums(artist_id=uri, limit=50, album_type='album', )
        result = []
        for album in albums['items']:
            result.append(
                {
                    "artist": album['artists'][0]['name'],
                    "images": self._get_image(album),
                    "name": album["name"],
                    "url": (album['external_urls']['spotify'])
                }
            )
        return result

    def get_list_track(self, url_album):
        album_info = self.spotify.album(url_album)
        album_tracks = self.spotify.album_tracks(album_id=url_album, limit=50)
        tracks = []
        for track in album_tracks['items']:
            tracks.append({
                "number": track['track_number'],
                "name": track['name'],
                "url": track["external_urls"]["spotify"]
            })

        result = {
            "artist_name": album_info["artists"][0]["name"],
            "album_name": album_info["name"],
            "album_tracks": tracks,
            "image_album": self._get_image(album_info)
        }
        return result

    def get_track_info(self, url_track):
        track = self.spotify.track(track_id=url_track)
        track_info = {
            'track_name': track['name'],
            'artist_name': track['artists'][0]['name'],
            'album_name': track['album']['name'],
            'image': self._get_image(track['album']),
            'album_url': track['album']['external_urls']['spotify']
        }
        return track_info
