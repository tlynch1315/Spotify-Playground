from config import *
import requests
import json

class Spotify:

    def __init__(self):
        self.apiKeys = {
            'tommy': API_TOKEN_TOMMY,
            'sarah': API_TOKEN_SARAH
        }
        self.userIds = {
            'tommy': 'tlynch1315',
            'sarah': '1218028720'
        }
        return

    def getHeaders(self, name):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.apiKeys.get(name.lower())}',
        }

    def getLikedSongs(self, name):
        headers = self.getHeaders(name)
        likedUris = set()
        uri = f'https://api.spotify.com/v1/me/tracks'
        while uri:
            responseJson = self.getLikedSongsByUri(uri, headers)
            uri = responseJson.get('next')
            items = responseJson.get('items')
            tracks = [item.get('track') for item in items]
            uris = [track.get('uri') for track in tracks]
            [likedUris.add(uri) for uri in uris]

        return likedUris

    def getLikedSongsByUri(self, uri, headers):
        response = requests.get(uri, headers=headers)
        return response.json()

    def createPlaylist(self, name, playlistName, public=False, collaborative=True):
        if public and collaborative:
            raise Exception('Cannot create public and collaborative playlist')
        userId = self.userIds.get(name.lower())
        headers = self.getHeaders(name)
        requestBody = {}
        requestBody['public'] = public
        requestBody['collaborative'] = collaborative
        requestBody['name'] = playlistName
        requestBody['description'] = '**** Add Description Here ****'
        url = f'https://api.spotify.com/v1/users/{userId}/playlists'
        postResponse = requests.post(url, json=requestBody, headers=headers)
        return postResponse.json()

    def addTracksToPlaylist(self, owner, url, uris):
        headers = self.getHeaders(owner)
        requestBody = {
            'uris': list(uris)
        }
        response = requests.post(url, json=requestBody, headers=headers)
        return response.json()

    def createJointPlayList(self, owner, names, playlistName):
        uris = set(spotify.getLikedSongs(names[0]))
        [uris.intersection_update(spotify.getLikedSongs(name)) for name in names[1:]]
        createResponse = self.createPlaylist(owner, playlistName)
        playlistUri = createResponse.get('href') + '/tracks'
        return self.addTracksToPlaylist(owner, playlistUri, uris)



if __name__ == "__main__":
    spotify = Spotify()
    print(spotify.createJointPlayList('tommy', ['tommy', 'sarah'], 'Coding Is Fun'))
