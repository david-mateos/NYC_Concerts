#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 09:45:53 2020

S1: Get all top artitsts
S2: Supplement with some related artists
S3: Make into csv

@author: davidmateos
"""
import os
import spotipy
import spotipy.util as util
import csv

USERNAME= '1297034112' 
SCOPE= 'user-top-read, user-follow-read' 
CLIENT_ID='219ee35238aa44cbbc6e3f303a799002'
CLIENT_SECRET= 'd6ce818e199440dda66d685bb1fd6c8c'
REDIRECT_URI= 'https://localhost:8080'

os.environ['SPOTIPY_CLIENT_ID'] = '219ee35238aa44cbbc6e3f303a799002'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'd6ce818e199440dda66d685bb1fd6c8c'


util.prompt_for_user_token(username=USERNAME,
                           scope=SCOPE,
                           client_id=CLIENT_ID,
                           client_secret=CLIENT_SECRET,
                           redirect_uri=REDIRECT_URI)

token = util.prompt_for_user_token(USERNAME, SCOPE)
sp = spotipy.Spotify(auth=token)
sp.trace = False

def get_my_followed_artists():
    artists = []
    my_artists = []
    results = sp.current_user_followed_artists()
    artists.extend(results['artists']['items'])
    while results['artists']['next']:
        results = sp.current_user_followed_artists(
                after=results['artists']['cursors']['after'])
        artists.extend(results['artists']['items'])
    for artist in artists:
        my_artists.append(artist['name'])
    return my_artists

t_ranges = ['short_term', 'medium_term', 'long_term']
artist_names = []
top_artists = []

if token:
    
    for i, range in enumerate(t_ranges):
        
        top_artists.append(sp.current_user_top_artists(time_range=range, 
                                                       limit=50))

        for k, item in enumerate(top_artists[i]['items']):
            
            artist_names.append(item['name']) 

    artist_names = get_my_followed_artists() + artist_names
    duplicates = set()
    for artist in artist_names:
        name = artist
    
        if name not in duplicates:
            duplicates.add(name)      

    artist_names = duplicates
    
    print(len(artist_names))
    
    '''
    with open('top_artists.csv','w', newline='') as result_file:
        wr = csv.writer(result_file, delimiter=',')
        wr.writerow(list(artist_names))
      '''
else:
    print('Could not get token.')   

