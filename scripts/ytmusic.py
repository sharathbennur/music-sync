from ytmusicapi import YTMusic
from pathlib import Path

parent_dir_path = Path(__file__).resolve().parents[1]
ytm = YTMusic("{}/data/browser.json".format(parent_dir_path.absolute()))

# play latest 10 liked songs
my_music = ytm.get_library_songs(limit=10)
for item in my_music:
    print(f"Title: {item['title']}")
    print(f"Artist: {item['artists'][0]['name']}")
    print(f"Album: {item['album']['name'] if 'album' in item else 'N/A'}")


