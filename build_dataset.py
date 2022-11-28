#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import os
import json
import re
from tqdm import tqdm
import numpy as np
import copy


# In[3]:


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
   
    return data

def enrich_song(song: dict, playlist: dict):
    """Playlist enrichment procedure"""
    song['playlist_name'] = playlist['name']
    song['playlist_mod_at'] = playlist['modified_at']
    song['playlist_num_followers'] = playlist['num_followers']
    song['user'] = playlist['pid']
    song['listened'] = True
    return song


# In[4]:


# Listing directory
files = os.listdir("./data")

# Regular expression for desired filenames
desired_filename = re.compile("mpd.*")

# Loading data
data = dataloader_pipeline(files, desired_filename)


# In[5]:


# Constructing a song centric dataset
print("Building Song Dataset...")
new_data = {"data": [enrich_song(song, playlist) for playlist in data for song in playlist['tracks']]}


# In[7]:


# Writing song centric dataset to file
print("Writing data to file...")
with open('full_song_data.json', 'w') as file_writer:
    json.dump(new_data, file_writer)


# In[8]:


# Splitting up to train and test, writing train and test to their own files
print("Splitting into train and test sets...")
my_data = new_data['data']
np.random.shuffle(my_data)

# Splitting train and test by threshold
split_threshold = int(len(my_data) * (0.75))
train = my_data[:800_000]

# Attaining positive instances
test_positives = my_data[800_000:1_000_000]


# In[9]:


# Constructing negative instances
print("Constructing negative instances...")
test_negatives = []

# Sampling negatives
for ex in test_positives:
    user = ex['user']
    random_song = ex
    
    # Sampling random songs until one found from different playlist
    while random_song['user'] == user:
        random_song = my_data[np.random.randint(0, len(my_data))]
    
    # Negative example modification
    neg_ex = copy.deepcopy(random_song)
    neg_ex['listened'] = False
    
    # Appending
    test_negatives.append(neg_ex)

test_positives += test_negatives


# In[10]:


# Writing song centric dataset to file
print("Writing training data to file...")
with open('data_train.json', 'w') as file_writer:
    json.dump(train, file_writer)


# In[ ]:





# In[11]:


# Writing song centric dataset to file
print("Writing test data to file...")
with open('data_test.json', 'w') as file_writer:
    json.dump(test_positives, file_writer)


# In[ ]:





# In[ ]:




