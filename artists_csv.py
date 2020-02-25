#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S1: Get all top artists
S2: Supplement with some artists you are following
S3: write unique names to a csv

@author: davidmateos
"""
#import os use to set env vars
import spotipy
import spotipy.util as util
import csv

USERNAME= '' # the targeted user
SCOPE= 'user-top-read, user-follow-read' 

REDIRECT_URI= 'https://localhost:8080'

os.environ['SPOTIPY_CLIENT_ID'] = '' # make sure to set these with your own
os.environ['SPOTIPY_CLIENT_SECRET'] = ''

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

    artist_names = get_my_followed_artists() + artist_names  #add artists you follow
    duplicates = set()
    for artist in artist_names:
        name = artist
        if name not in duplicates:
            duplicates.add(name)      

    artist_names = duplicates
    
    # now write a csv file to read into R script
    with open('top_artists.csv','w', newline='') as result_file:
        wr = csv.writer(result_file, delimiter=',')
        wr.writerow(list(artist_names))
      
else:
    print('Could not get token.')   
