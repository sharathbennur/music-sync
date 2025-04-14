import pickle
from pathlib import Path
from ytmusicapi import YTMusic
from utils import YTM_Song, album_name, get_sync_status, in_library, is_explicit
from pprint import pprint


parent_dir_path = Path(__file__).resolve().parents[1]
ytm = YTMusic("browser.json")
print(ytm.get_account_info())


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
                    try:
                        search_result_list.append(YTM_Song(
                            artists = result['artists'],
                            index = ind,
                            album_name = album_name(result),
                            type = result['resultType'],
                            song_title = result['title'],
                            in_library = in_library(result),
                            is_explicit = is_explicit(result),
                            duration = result['duration'],
                            video_id = result['videoId']))
                    except KeyError:
                        print(result)

    return search_result_list


def q_replace_song(search_result_list: list) -> dict:
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

def q_which_song(search_result_list: list)-> int:
    """
    Utility function to decide which track the should be liked if multiple options are 
    available 
    """
    q_text = "Select which song to 'LIKE' from the options below:"
    for idx, song in enumerate(search_result_list):
        song_artists = ""
        if song.type == 'song':
            for artist in song.artists:
                song_artists = song_artists.join([song_artists, ('' if not song_artists else '+'),  artist['name']]).strip()
                # song_artists = song_artists.join([song_artists, '+', artist['name']]) 
            explicit_label = "(E)" if song.is_explicit else ""
            song_text = "{}{}.{}-{}-{}".format(idx,
                                                explicit_label,
                                                song.song_title, 
                                                song_artists, 
                                                song.album_name)
            q_text = '\n'.join([q_text, song_text])
    print(q_text)
    selected_song = input("Select song # or 'e' to: ")
    if selected_song:
        try:
            return int(selected_song)
        except ValueError:
            return None


def validate_rate_song(index: int, 
                       search_result_list: list):
    """
    Utility function to validate if index is correct and "LIKE" song by index
    """
    if index != None:
        replacement_song = search_result_list[index]
        try:
            artist_names = [x["name"] for x in replacement_song.artists]
            song_string = "{}: {}".format(" & ".join(artist_names),
                                         replacement_song.song_title)
            print(song_string)
            ytm.rate_song(videoId=replacement_song.video_id, rating="LIKE")
            print("Saved {} to liked music".format(song_string))
            return True
        except Exception as e:
            print("Could not save song: {}".format(e))
            return False
    else:
        print("No song selected, moving along...")
        return True
        

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
        synced = get_sync_status(item)
        if not synced:
            search_result_list = get_yt_search_results(item)
            # if you have search results - you get a list back
            if search_result_list:
                test_results = q_replace_song(search_result_list)
                if test_results["in_library"] and not test_results["is_explicit"]:
                    # if we have it in the lib but its not the explicit version
                    replacement_song_index = q_which_song(search_result_list)
                    synced = validate_rate_song(replacement_song_index, search_result_list)
                    print("Synced")
                elif test_results["in_library"] and test_results["is_explicit"]:
                    # if its already in the library and is explcit
                    pass
                else:
                    # if we don't have it in the libarary
                    replacement_song_index = q_which_song(search_result_list)
                    synced = validate_rate_song(replacement_song_index, search_result_list)
                    print("Synced")
            else:
                pass
            # if we did successfuly sync this track to YTMusic
            if synced:
                item["done"] = True
                spotify_library[idx] = item
                with open('{}/data/spotify_saved_tracks.pickle'.format(parent_dir_path.absolute()), 'wb') as file:
                    pickle.dump(spotify_library, file)
                    print("saved updated to pickle file")
        

sync_sp_ytm()