
from google import genai

import os
from dotenv import load_dotenv
import genreScraper
import requests
import json

all_genres = genreScraper.genres


load_dotenv()
class SpotifyInterface:

    def __init__(self):

        self.geminiClient = genai.Client()


    
    def get_genres(self, prompt):
        
        genres_text = ", ".join(all_genres)

        text = f"""
        You are a music assistant. 
        From the following list of genres:
        {genres_text}

        Select exactly 5 genres that best match this mood: "{prompt}"
        Output only a comma seperated list of genres, for example make sure the complete word is there and no letter is deleted:
        acoustic, lo-fi, folk, indie, singer-songwriter
        """
        response = self.geminiClient.models.generate_content(model="gemini-2.5-flash", contents=text).text

        return response.split(',') 

    
    def get_intro_playlist(self,genre):
        
        playlist_name = "the sound of " +genre.title()
        print("Searching for playlist:", playlist_name)
        # Search for a public playlist named playlist_name created by 'particle detector'
        results = self.sp.search(q=f'playlist:{playlist_name}', type='playlist', limit=20)
        print(results["playlists"]['items'])
        for i in results["playlists"]['items']:
            if i:
                if i['owner']['id'] == 'thesoundsofspotify':
                    print("Found playlist:", i['name'], i['external_urls']['spotify'])
                
        return





def create_mixed_playlist(access_token,genres, playlist_name="Moodify Mix"):
    base_url = "https://api.spotify.com/v1"
    headers = {"Authorization": f"Bearer {access_token}"}

    # get current user id
    user_resp = requests.get(f"{base_url}/me", headers=headers).json()
    user_id = user_resp["id"]

    all_tracks = []

    for genre in genres:
        # find intro playlist
        playlist_link = genreScraper.get_intro_playlist(genre)
        # extract playlist id from the playlist link
        playlist_id = playlist_link.split('/')[-1]
        if not playlist_id:
            continue

        # fetch top 10 tracks
        tracks_url = f"{base_url}/playlists/{playlist_id}/tracks"
        tracks_resp = requests.get(tracks_url, headers=headers, params={"limit": 10}).json()
        track_uris = [t['track']['uri'] for t in tracks_resp.get('items', []) if t.get('track')]
        all_tracks.extend(track_uris)

    # create a new playlist
    create_url = f"{base_url}/users/{user_id}/playlists"
    payload = {
        "name": playlist_name,
        "description": f"A mix of genres: {', '.join(genres)}",
        "public": True
    }
    new_playlist = requests.post(create_url, headers=headers, json=payload).json()
    playlist_id = new_playlist["id"]

    # add songs (100 per batch max)
    add_url = f"{base_url}/playlists/{playlist_id}/tracks"
    for i in range(0, len(all_tracks), 100):
        chunk = all_tracks[i:i+100]
        requests.post(add_url, headers=headers, json={"uris": chunk})

    return new_playlist['external_urls']['spotify']


