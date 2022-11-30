#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import json
import re
from tqdm import tqdm
import numpy as np
import copy
from collections import defaultdict


# In[2]:


def dataloader_pipeline(file_list: list, desired_filename) -> list:
    """
    Pipeline for loading in data
    
    @param file_list: A list of files to load in
    @returns data: A list of playlists from these files
    """
    # Resulting data (hopefully to be stored in list)
    data = []
    
    # Traversing through available datafiles
    print("Starting Dataloading...")
    for file in tqdm(file_list):
        
        # Ensuring filename valid
        if desired_filename.match(file):
            
            # Opening and preprocessing
            with open("./data/" + file, 'r') as file_reader:
                data += json.load(file_reader)["playlists"]
    
    print("Finished Dataloading...")
   
    return data[:200000]

def build_relevant_ds(songs: list):
    """
    Preprocesses data, simultaneously building relevant data structures
    
    @param data - a data list of playlist dictionaries to preprocess
    @returns a list of tracks per user, users per track, watered down data list
    """
    
    def process_uri(uri:str):
        """URI Processing method"""
        return uri.split(":")[2]
        
    print("Preprocessing started...")
    tracks_per_user, users_per_track, users_per_artist, artists_per_user = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    
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

    return tracks_per_user, users_per_track, users_per_artist, artists_per_user

def enrich_song(song: dict, playlist: dict):
    """Playlist enrichment procedure"""
    song['playlist_name'] = playlist['name']
    song['playlist_mod_at'] = playlist['modified_at']
    song['playlist_num_followers'] = playlist['num_followers']
    song['user'] = playlist['pid']
    song['listened'] = True
    return song


# In[3]:


# Listing directory
files = os.listdir("./data")

# Regular expression for desired filenames
desired_filename = re.compile("mpd.*")

# Loading data
data = dataloader_pipeline(files, desired_filename)


# In[4]:


# Constructing a song centric dataset
print("Building Song Dataset...")
new_data = {"data": [enrich_song(song, playlist) for playlist in data for song in playlist['tracks']]}


# In[7]:


# Writing song centric dataset to file
print("Writing data to file...")
with open('full_song_data.json', 'w') as file_writer:
    json.dump(new_data, file_writer)


# In[5]:


# Splitting up to train and test, writing train and test to their own files
print("Splitting into train and test sets...")
my_data = new_data['data']
np.random.shuffle(my_data)

# Splitting train and test by threshold
split_threshold = int(len(my_data) * (0.75))
train = my_data[:200_000]

# Attaining positive instances
test_positives = my_data[800_000:1_000_000]


# In[6]:


# Writing song centric dataset to file
print("Writing training data to file...")
with open('data_train.json', 'w') as file_writer:
    json.dump(train, file_writer)


# In[7]:


print(f"Test Set Size: {len(test_positives)}")


# In[8]:


# Writing song centric dataset to file
print("Writing test data to file...")
with open('data_test.json', 'w') as file_writer:
    json.dump(test_positives, file_writer)


# In[ ]:





# In[ ]:




