import pickle
from pathlib import Path
from ytmusicapi import YTMusic
from pprint import pprint

parent_dir_path = Path(__file__).resolve().parents[1]
ytm = YTMusic("{}/data/browser.json".format(parent_dir_path.absolute()))

def sync_sp_ytm():
    with open("{}/data/spotify_saved_tracks.pickle".format(parent_dir_path.absolute()), 'rb') as pickle_file:
        spotify_library = pickle.load(pickle_file)
    for idx, item in enumerate(spotify_library):
        # pprint(item)
        if idx == 1:
            if item["type"]=="track":
                search_string = "{} {} {}".format(item['album']['artists'][0]['name'],
                                                item['album']['name'],
                                                item["name"])
                print_string = "{}-{}-{}".format(item['album']['artists'][0]['name'],
                                                item['album']['name'],
                                                item["name"])
                print("Searching: ", print_string)
                search_result = ytm.search(search_string)
                pprint(search_result)
            else:
                print("Album")
        

sync_sp_ytm()