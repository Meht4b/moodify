import spotipy

from google import genai
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import genreScraper

all_genres = genreScraper.genres


load_dotenv()
class SpotifyInterface:

    def __init__(self):

        CLIENT_ID = load_dotenv("SPOTIPY_CLIENT_ID")
        CLIENT_SECRET = load_dotenv("SPOTIPY_CLIENT_SECRET")
        REDIRECT_URI = "https://127.0.01:8888/callback"
        scope = "playlist-modify-public playlist-modify-private user-library-read"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                            client_secret=CLIENT_SECRET,
                                                            redirect_uri=REDIRECT_URI,
                                                            scope=scope,
                                                            cache_path=".spotify_token_cache"))
        self.geminiClient = genai.Client()
        

    
    def create_playlist(self,prompt):
        songs = self.get_songs(prompt)

        seed_track_ids = []
        for song in songs:
            try:
                results = self.sp.search(q=song, type='track', limit=1)
                if results['tracks']['items']:
                    print(results['tracks']['items'][0])
                    return
                    track_id = results['tracks']['items'][0]['id']
                    seed_track_ids.append(track_id)
            except Exception as e:
                pass
        
        seed_track_ids = []
        derived_genres = set()

        for song in songs:
            results = self.sp.search(q=song, type="track", limit=1)
            if results["tracks"]["items"]:
                track = results["tracks"]["items"][0]
                seed_track_ids.append(track["id"])

                # Get artist ID → fetch genres
                artist_id = track["artists"][0]["id"]
                artist_info = self.sp.artist(artist_id)
                if "genres" in artist_info:
                    derived_genres.update(artist_info["genres"])

        print("🎶 Found seed tracks:", seed_track_ids)
        print("🎼 Derived genres:", list(derived_genres))

        # ----------------------------
        # 3. Get Recommendations
        # ----------------------------

        # ----------------------------
        # 4. Create Playlist
        # ----------------------------
        user_id = self.sp.current_user()["id"]
        playlist = self.sp.user_playlist_create(user=user_id, name=prompt, public=True)

        all_tracks = seed_track_ids 
        self.sp.playlist_add_items(playlist["id"], all_tracks)

        print("\n✅ Playlist created!")
        print("👉 Open in Spotify:", playlist["external_urls"]["spotify"])

    def get_songs(self, prompt):
        prompt = f"Generate a list of 10 songs with their artists based on the following theme: {prompt}. Format the response as Song Title - Artist Name separated by commas."
        response = self.geminiClient.models.generate_content(model="gemini-1.5-flash", contents=prompt)

        song_list = response.text
        songs = [song.strip() for song in song_list.split(',')]
        return songs
 
    def get_genres(self, prompt):
        prompt = f"select 5 genres from this list {all_genres} that matches the following theme: '{prompt}',give it as a comma separated list, make sure the whole word is finished."
        response = self.geminiClient.models.generate_content(model="gemini-1.5-flash", contents=prompt)

        genre_list = response.text
        
        genres = [genre.strip().lower() for genre in genre_list.split(',')]
        return genres
    
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

        playlist = results['playlists']['items'][0]
        print("Found playlist:", playlist['name'], playlist['external_urls']['spotify'])
        return playlist

    def create_playlist_from_genres(self,prompt):
        genres = self.get_genres(prompt)
        print("Selected genres:", genres)    
        playlists = list(map(self.get_intro_playlist, genres))

        for i in playlists:
            if i:
                print(i['external_urls']['spotify'])

        return 1

        track_ids = []
        for playlist in playlists:
            results = self.sp.playlist_items(playlist['id'])
            for ind in range(min(10,len(results['items']))):
                track = results['items'][ind]['track']
                track_ids.append(track['id'])

        for i in track_ids:
            print(i)

a = SpotifyInterface()
a.create_playlist("chill summer vibes")
