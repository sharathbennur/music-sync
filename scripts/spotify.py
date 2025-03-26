import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import pickle

load_dotenv()

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Get the first page of saved tracks
results = sp.current_user_saved_tracks()
# print first page of saved tracks
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

all_tracks = []

# Iterate through all pages of saved tracks
while results:
    for item in results['items']:
        track = item['track']
        all_tracks.append(track)
    if results['next'] is not None:
        results = sp.next(results)
    else:
        results = None

print(len(all_tracks))
with open('spotify_saved_tracks.pickle', 'wb') as file:
    pickle.dump(all_tracks, file)
    