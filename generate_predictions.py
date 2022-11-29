import pandas as pd
import numpy as np
from collections import defaultdict

def generate_predictions(some_tracks: list, data_train: pd.DataFrame):
  """Generates predictions using hybrid user artist model"""
  # Prediction array
  predictions = []

  # Encriching data, building data structures
  tracks_per_user_g, users_per_track_g, users_per_artist_g, artists_per_user_g, artists_per_song = build_relevant_ds_generate(data_train[:200_000])

  # For each track building recommendations by finding a similar user
  for track in some_tracks:
    artist = track['artist_name']
    songs = {track['track_name'] for track in some_tracks}
    sims = []

    # finding most similar user who has also listened to artist
    for ext_user in users_per_artist_g[artist]:
      sims.append((jaccard(songs, set(tracks_per_user_g[user])), ext_user))

    # If have found similar user
    if len(sims) != 0:
      closest_user = max(sims)

      # Randomly selecting from closest user tracks
      closest_user_tracks = tracks_per_user_g[closest_user[1]]

      # Predicting novel songs
      choice = predictions[0][0] if len(predictions) > 0 else ""
      s_artist = predictions[0][0] if len(predictions) > 0 else ""
      iter = 0

      while (choice, s_artist) in predictions and iter < 5:
        iter += 1
        choice = closest_user_tracks[np.random.randint(len(closest_user_tracks))]
        s_artist = artists_per_song[choice][0] if choice in artists_per_song else [""]
      
      if(iter < 5):
        predictions.append((choice, s_artist))

  return predictions[1:11]


def build_relevant_ds_generate(songs: list):
    """
    Preprocesses data, simultaneously building relevant data structures
    
    @param data - a data list of playlist dictionaries to preprocess
    @returns a list of tracks per user, users per track, watered down data list
    """
    
    def process_uri(uri:str):
        """URI Processing method"""
        return uri.split(":")[2]
        
    print("Preprocessing started...")
    tracks_per_user, users_per_track, users_per_artist, artists_per_user, artists_per_song = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    
    # Traversing through data and preprocessing
    for song in songs:

      # Obtaining user
      user = song['user']

      # obtaining necessary data
      track, artist, album = song['track_name'], song['artist_name'], song['album_name']
      
      # Appending data to data structures
      tracks_per_user[user].append(track)
      users_per_track[track].append(user)
      users_per_artist[artist].append(user)
      artists_per_user[user].append(artist)
      artists_per_song[track].append(artist)
            
    return tracks_per_user, users_per_track, users_per_artist, artists_per_user, artists_per_song
            
