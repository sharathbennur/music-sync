import pickle
from pathlib import Path
from ytmusicapi import YTMusic
from pprint import pprint

from utils import YTM_Song

parent_dir_path = Path(__file__).resolve().parents[1]
ytm = YTMusic("{}/data/browser.json".format(parent_dir_path.absolute()))


def get_yt_search_results(item) -> list[YTM_Song]:
    """
    Utility function to search for a track from Spotify and return the results in a 
    readable format
    """
    # setup
    search_result_list = []

    # search if track
    if item["type"]=="track":
        search_string = "{} {} {}".format(item['album']['artists'][0]['name'],
                                        item['album']['name'],
                                        item["name"])
        print_string = "{}-{}-{}".format(item['album']['artists'][0]['name'],
                                        item['album']['name'],
                                        item["name"])
        print("Searching: ", print_string)
        search_results = ytm.search(search_string)

        # parse search results to easily read them
        if search_results:
            for ind, result in enumerate(search_results):
                if result['resultType']=="song":
                    search_result_list.append(YTM_Song(
                        artists = result['artists'],
                        index = ind,
                        album_name = result['album']['name'],
                        type = result['resultType'],
                        song_title = result['title'],
                        in_library = result['inLibrary'],
                        is_explicit = result['isExplicit'],
                        duration = result['duration'],
                        video_id = result['videoId']))

    return search_result_list


def test_replace_song(search_result_list: list) -> dict:
    """
    Utility function to ask user if the current track in the playlist should be replaced
    with a different track 
    """
    in_library = False
    is_explicit = False
    if len(search_result_list)>0:     
        # display first 5 results to choose between them
        for ytm_song in search_result_list:
            # check to see if we already have the song in the library
            # and if there is an explicit version available
            if ytm_song.in_library:
                in_library = True
            if ytm_song.is_explicit:
                is_explicit = True
    return {
        "in_library": in_library,
        "is_explicit": is_explicit 
    }

def q_replace_song(search_result_list):
    """
    Utility function to decide which track the should be liked if multiple options are 
    available 
    """
    


"""
Psuedocode:
- Search for song in Spotity playlist on YTMusic
- If the song is already in your YTMusic liked songs and passes our explicit filter- move on
- If not - ask the user if they want to:
    a. Do nothing (assuming there are options)
        - If they chose to do nothing (a) - move on
    b Or replace it with one of the explicit options
        - if they chose to replace it - ask which one
- If replace_song > then replace it with selected_song by liking selected song
"""

def sync_sp_ytm():
    with open("{}/data/spotify_saved_tracks.pickle".format(parent_dir_path.absolute()), 'rb') as pickle_file:
        spotify_library = pickle.load(pickle_file)
    for idx, item in enumerate(spotify_library):
        # for now just index==1
        if idx == 1:
            search_result_list = get_yt_search_results(item)
            # if you have search results - you get a list back
            if search_result_list:
                test_results = test_replace_song(search_result_list)
                if test_results["in_library"] and not test_results["is_explicit"]:
                    replacement_song = q_replace_song(search_result_list)
                elif test_results["in_library"] and test_results["is_explicit"]:
                    pass
                else:
                    replacement_song = q_replace_song(search_result_list)
        else:
            print("Album")
        

sync_sp_ytm()