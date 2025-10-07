import requests
from bs4 import BeautifulSoup
from google import genai
import os
from dotenv import load_dotenv
import genreScraper
import requests
import json
import pandas as pd

all_genres = genreScraper.genres

load_dotenv()
class SpotifyInterface:
    def __init__(self,access_token):

        self.geminiClient = genai.Client()
        self.access_token = access_token
        self.spotify_features = pd.read_csv("backend/SpotifyFeatures.csv")

    def get_genres(self,prompt):
        
        response = self.geminiClient.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"give me a list of 20 specific spotify genres as a comma seperated list for the prompt make sure they are there in the site https://everynoise.com/ do not give anything else just the genres eg: jazz,classical,..: {prompt}"
        )

        return response.text.split(',')
    
    def get_intro_playlist(self,genre):
        try:
            genre = genre.replace(' ', '')
            genre= genre.replace('-','')
            genre = genre.replace('-','')
            genre = genre.lower()
            url = f"https://everynoise.com/engenremap-{genre}.html"
            resp = requests.get(url)
            resp.raise_for_status()
            html = resp.text
            soup = BeautifulSoup(html, "html.parser")
            header = soup.find("div", class_="title")
            if header is None:
                return None
            if header.find_all("a").__len__() < 4:
                return None
            return header.find_all("a")[3]['href']
        except Exception as e:
            print(e)
            return None

    def get_sound_playlist(self,genre):
            try:
                genre = genre.replace(' ', '')
                genre= genre.replace('-','')
                genre = genre.replace('-','')
                genre = genre.lower()
                url = f"https://everynoise.com/engenremap-{genre}.html"
                resp = requests.get(url)
                resp.raise_for_status()
                html = resp.text
                soup = BeautifulSoup(html, "html.parser")
                header = soup.find("div", class_="title")
                if header is None:
                    return None
                if header.find_all("a").__len__() < 4:
                    return None
                return header.find_all("a")[2]['href']
            except Exception as e:
                print(e)
                return None

    def get_pulse_playlist(self,genre):
            try:
                genre = genre.replace(' ', '')
                genre= genre.replace('-','')
                genre = genre.replace('-','')
                genre = genre.lower()
                url = f"https://everynoise.com/engenremap-{genre}.html"
                resp = requests.get(url)
                resp.raise_for_status()
                html = resp.text
                soup = BeautifulSoup(html, "html.parser")
                header = soup.find("div", class_="title")
                if header is None:
                    return None
                if header.find_all("a").__len__() < 4:
                    return None
                return header.find_all("a")[4]['href']
            except Exception as e:
                print(e)
                return None

    def create_name(self,prompt):

        response = self.geminiClient.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"summarise this in two or three words {prompt}"
        )

        return "Moodify Mix: "+ response.text

    def create_desc(self,prompt):

        response = self.geminiClient.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"give a suitable playlist description for the prompt,only return the name nothing else {prompt}"
        )

        return response.text

    def create_playlist(self,prompt):
        genres = self.get_genres(prompt)
        playlist_tracks = []

        for genre in genres:
            intro_url = self.get_intro_playlist(genre)
            sound_url = self.get_sound_playlist(genre)
            pulse_url = self.get_pulse_playlist(genre)
            urls = [intro_url, sound_url, pulse_url]
            for url in urls:
                if url and "open.spotify.com/playlist/" in url:
                    playlist_id = url.split("playlist/")[1].split("?")[0]
                    headers = {
                        "Authorization": f"Bearer {self.access_token}"
                    }
                    tracks_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=5"
                    resp = requests.get(tracks_endpoint, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        for item in data.get("items", []):
                            track = item.get("track")
                            if track and track.get("id"):
                                playlist_tracks.append(track["id"])

        # Remove duplicates and limit to 100 tracks (Spotify API limit)
        unique_tracks = list(dict.fromkeys(playlist_tracks))[:100]

        # Create a new playlist
        user_profile = requests.get(
            "https://api.spotify.com/v1/me",
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        user_id = user_profile.json()["id"]

        playlist_data = {
            "name": self.create_name(prompt),
            "description": self.create_desc(prompt),
            "public": False
        }
        create_playlist_resp = requests.post(
            f"https://api.spotify.com/v1/users/{user_id}/playlists",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            },
            data=json.dumps(playlist_data)
        )
        print(create_playlist_resp.json())
        playlist_id = create_playlist_resp.json()["id"]

        # Add tracks to the new playlist in batches of 100
        if unique_tracks:
            requests.post(
                f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                },
                data=json.dumps({"uris": [f"spotify:track:{tid}" for tid in unique_tracks]})
            )

        return playlist_id


if __name__ == "__main__":

    a = SpotifyInterface("BQCjE6XqSfwt4R7NnXqV5P4YP17hPeu3a3EJCCqH6x9zqR8DjGExgTmuFOs0GC7Lreeg0vB9cS-9kIooBvzo-DMhJyqP4dSlkXK-tlrVns0ZEbXX-0pmwm2Pb5YREf-eVHQ0GihnoO01hRaVt0OtpIL6PCHu5cC1HL27jQSQatZXl3Jf30NuqoeuApK2Gh57rKtx8A0s0PzNPWGLbSobj96QqI7tTCmw-OtKAffw3KA8fxhhVOEmgULAQHMcu21sEdPs3isGiiwmVUhqnuG2Lq4olGaFqdhfV0YEPrP3iqTvNMftnT4094ALQNBuYbCD7GruINNWvPA6YxLvVIAVD04")
    genres = a.get_genres("riding into the sunset feeling all happy with life give something that feels like you are floating something with lots of depth and makes you feel like music is coming from all around ")
    print(genres)
    a.create_playlist(genres)