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

