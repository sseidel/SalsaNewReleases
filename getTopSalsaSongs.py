import requests
import re


headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }


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
    number_of_top_songs = 10
    for n in range(1, number_of_top_songs + 1):
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
for site in range(1,number_of_main_pages_to_scan):
  actual_url = f"{url}page/{site}/"
  songs = songs.union(get_playlist_urls(actual_url))
for s in songs:
    print(s)
