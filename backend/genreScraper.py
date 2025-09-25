import requests
from bs4 import BeautifulSoup

def get_genre_div_texts(url="https://everynoise.com/"):
    resp = requests.get(url)
    resp.raise_for_status()
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    genre_divs = soup.find_all("div", class_="genre")
    texts = [div.get_text(strip=True) for div in genre_divs]

    genres = [t.strip()[:-2] for t in texts]

    return genres
    
