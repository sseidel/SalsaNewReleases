import requests
import re
import html
import time
import json

BASE_URL = "https://www.newgensalsa.com/page/{}/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Regex to extract title + URL
POST_PATTERN = re.compile(
    r'<h2 class="cb-post-title">\s*<a href="([^"]+)">(.+?)</a>',
    re.DOTALL
)

def fetch_page(page):
    url = BASE_URL.format(page)
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return None
    return response.text


def parse_entries(html_text):
    results = []

    matches = POST_PATTERN.findall(html_text)

    for url, raw_text in matches:
        text = html.unescape(raw_text.strip())

        # Extract year
        year_match = re.search(r"\((\d{4})\)$", text)
        year = year_match.group(1) if year_match else None

        if year:
            text = text[:text.rfind("(")].strip()

        # Split by separator
        parts = [p.strip() for p in text.split("·")]

        if len(parts) >= 2:
            song = parts[0]
            artists = parts[1:]
        else:
            song = text
            artists = []

        results.append({
            "song": song,
            "artists": artists,
            "year": year,
            "url": url
        })

    return results


def scrape_all(max_pages=50, delay=1):
    all_results = []
    seen = set()

    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")

        html_text = fetch_page(page)
        if not html_text:
            break

        entries = parse_entries(html_text)

        if not entries:
            break

        for e in entries:
            key = (e["song"], tuple(e["artists"]))
            if key not in seen:
                seen.add(key)
                all_results.append(e)

        time.sleep(delay)

    return all_results


def main():
    data = scrape_all(max_pages=100)

    print(f"Total songs: {len(data)}")

    with open("songs.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()