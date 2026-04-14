import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime


YEAR = 2026
STARTDATE = datetime(YEAR,1,1)
CACHE = '.spotipyoauthcache'
# replace with our own playlist
playlist_id = "41EiuGEElMVvM8BAZDwfDk"
# insert your own client_id
CLIENT_ID = ""
# insert your own client_secret
CLIENT_SECRET = ""
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



def get_date_of_item(item):
    year = int(item['album']['release_date'].split('-')[0])
    month = int(item['album']['release_date'].split('-')[1])
    day = int(item['album']['release_date'].split('-')[2])
    return datetime(year, month, day)

def clean_up(input_string):
    words_to_replace = [ "Offical", "Oficial", "oficial", "Video", str(YEAR), "(", ")"]
    clean_word = input_string
    for word in words_to_replace:
        clean_word = clean_word.replace(word, "")
    return clean_word

filename = "songs.json"

with open(filename) as file:
    data = json.load(file)

songs = [ {"title":entry['song'].split('–')[0].strip(),"artist":entry['song'].split('–')[1].strip()} for entry in data if entry['year'] == str(YEAR) and '–' in entry['song'] ]
songs2 = [ {"title":entry['song'].split('-')[0].strip(),"artist":entry['song'].split('-')[1].strip()} for entry in data if entry['year'] == str(YEAR) and '-' in entry['song'] ]
video_songs = [ {"title":entry['song'].split('–')[0].strip(),"artist":clean_up(entry['song'].split('–')[1]).strip()} for entry in data if str(YEAR) in entry['song'] and '–' in entry['song'] ]
video_songs2 = [ {"title":entry['song'].split('-')[0].strip(),"artist":clean_up(entry['song'].split('-')[1]).strip()} for entry in data if str(YEAR) in entry['song'] and '-' in entry['song'] ]


playlist_details = sp.playlist_items(playlist_id)
uris = [ item['item']['uri'] for item in  playlist_details['items']  ]


for song in songs + songs2 + video_songs+ video_songs2:
    artist =song['artist']
    title = song['title']
    query = f"track:{title} artist:{artist}"
    print(query)
    result = sp.search(q=query, type="track", limit=1)
    print(result)
    if len(result['tracks']['items']):
        item = result['tracks']['items'][0]
        release_date = get_date_of_item(item)
        uri = item['uri']
        if uri not in uris and STARTDATE < get_date_of_item(result['tracks']['items'][0]):
            sp.playlist_add_items(playlist_id,[uri])
