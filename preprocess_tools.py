# Functional Utility file maintaining necessary data preprocessing scripts

import os
import json
import re
from tqdm import tqdm
from collections import defaultdict


def dataloader_pipeline(file_list: list) -> list:
    """
    Pipeline for loading in data

    @param file_list: A list of files to load in
    @returns data: A list of playlists from these files
    """
    # Resulting data (hopefully to be stored in list)
    data = []
    
    # Regular expression for desired filenames
    desired_filename = re.compile("mpd.*")

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

    
def build_relevant_ds(data: list):
    """
    Preprocesses data, simultaneously building relevant data structures
    
    @param data - a data list of playlist dictionaries to preprocess
    @returns a list of tracks per user, users per track, watered down data list
    """
    
    def process_uri(uri:str):
        """URI Processing method"""
        return uri.split(":")[2]
        
    
    print("Preprocessing started...")
    tracks_per_user, users_per_track, users_per_artist  = defaultdict(list), defaultdict(list), defaultdict(list)
    
    # Traversing through data and preprocessing
    for playlist in data:       
        user = playlist['pid']
        for track in playlist['tracks']:
            # obtaining necessary data
            track, artist, album = track['track_name'], track['artist_name'], track['album_name']
            
            # Appending data to data structures
            tracks_per_user[user].append(track)
            users_per_track[track].append(user)
            users_per_artist[artist].append(user)
            
    return tracks_per_user, users_per_track, users_per_artist
            
