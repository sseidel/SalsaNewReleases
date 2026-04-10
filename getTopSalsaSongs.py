import requests
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CACHE = '.spotipyoauthcache'
# create this at https://developer.spotify.com/dashboard
CLIENT_ID = ""
# create this at https://developer.spotify.com/dashboard
CLIENT_SECRET = ""
PLAYLIST_ID = ""
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }
auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="https://www.google.com/",
    open_browser=False,
    cache_path=CACHE,
    scope="playlist-modify-public"
)
token_info = auth_manager.get_cached_token()
access_token = auth_manager.get_access_token()
sp = spotipy.Spotify(auth_manager=auth_manager)
sp.trace = True

def get_playlist_urls(url):
    response = requests.get(url, headers=headers, timeout=10)
    html = response.text
    urls = set(re.findall(r"href=\"(https://www.newgensalsa.com/newgensalsa.*?)\"",html))
    print(urls)
    songs = set()
    for url in urls:
     try:
        new_songs = get_songs(url)
        songs = songs.union(new_songs)
        print("got the songs:")
     except Exception:
        print("exception")
    return songs

def get_songs(url):
    print(url)
    songs = set()
    response = requests.get(url, headers=headers, timeout=10)
    html = response.text
    tables = re.findall(r"<table.*?>(.*?)</table>", html, re.DOTALL)
    table = tables[0]
    rows = re.findall(r"<tr>(.*?)</tr>", table, re.DOTALL)
    for n in range(1,11):
      column_string = rows[n]
      columns = re.findall(r"<td>(.*?)</td>", column_string, re.DOTALL)
      song_titel = columns[1]
      artist_name = columns[2]
      song_tuple = (song_titel, artist_name)
      songs.add(song_tuple)

    return songs


url = "https://www.newgensalsa.com/category/salsaplaylist/"
number_of_main_pages_to_scan = 5
songs = set()
for site in range(1,number_of_main_pages_to_scan+1):
  actual_url = f"{url}page/{site}/"
  songs = songs.union(get_playlist_urls(actual_url))

for title, artist in songs:
    
    query = f"track:{title} artist:{artist}"
    print(query)
    result = sp.search(q=query, type="track", limit=1)
    if len(result['tracks']['items']):
     uri = result['tracks']['items'][0]['uri']
     print(f"uri: {uri}")
     sp.playlist_add_items(PLAYLIST_ID,[uri])
