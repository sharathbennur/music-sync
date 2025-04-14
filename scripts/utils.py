from typing import NamedTuple


class YTM_Song(NamedTuple):
    index: int
    artists: list
    album_name: str
    type: str
    song_title: str
    in_library: bool
    is_explicit: bool
    duration: str
    video_id: str

def album_name(result: dict):
    try: 
        return result['album']['name']
    except KeyError or TypeError:
        return "no album name"
    

def in_library(result: dict):
    try: 
        return result['inLibrary']
    except KeyError:
        return False


def is_explicit(result: dict):
    try: 
        return result['isExplicit']
    except KeyError:
        return False
    

def get_sync_status(item):
    try:
        return item["done"]
    except KeyError:
        return False