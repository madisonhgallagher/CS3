# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 11:51:13 2025

@author: Student
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import html  # For decoding HTML entities

# Your Genius API access token (replace with your token)
ACCESS_TOKEN = "ki9ZAMbXKmUhGRZrWrAt87sB7SvqPbdBUh_UZpG5J4TBnoPgdDvlToJEsUXiC9XA"
BASE_URL = "https://api.genius.com"

# List of songs (title, artist)
songs_list = [
    ("I’m The Problem", "Morgan Wallen"),
    ("By Myself (feat. Rod Wave)", "Lil Baby & Rylo Rodriguez"),
    ("Dum, Dumb, and Dumber", "Lil Baby, Young Thug & Future"),
    ("F U 2x", "Lil Baby"),
    ("30 For 30 (with Kendrick Lamar)", "SZA"),
    ("luther", "Kendrick Lamar & SZA"),
    ("Heart Of A Woman", "Summer Walker"),
    ("Residuals", "Chris Brown"),
    ("25", "Rod Wave"),
    ("Little Things", "Ella Mai"),
    ("Holy Ground", "BigXthaPlug & Jessie Murph"),
    ("Freestyle", "Lil Baby"),
    ("Stiff Gang", "Lil Baby"),
    ("Smile", "Morgan Wallen"),
    ("In A Minute", "Lil Baby"),
    ("WHATCHU KNO ABOUT ME", "GloRilla & Sexyy Red"),
    ("Low Down", "Lil Baby"),
    ("Sum 2 Prove", "Lil Baby"),
    ("Mo Chicken (feat. French Montana)", "Bossman Dlow"),
    ("Passport Junkie", "Rod Wave"),
    ("Help Me", "Real Boston Richey"),
    ("I LUV HER", "GloRilla & T-Pain"),
    ("March Madness", "Future"),
    ("99", "Lil Baby & Future"),
    ("LIKE ME (feat. 42 Dugg & Lil Baby)", "Future")
]






# Function to search for song on Genius API
def search_song(song_title, artist_name):
    search_url = f"{BASE_URL}/search"
    query = f"{song_title} {artist_name}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"q": query}
    
    response = requests.get(search_url, headers=headers, params=params)
    response.encoding = 'utf-8'  # Ensure UTF-8 decoding
    response.raise_for_status()
    data = response.json()
    
    hits = data.get("response", {}).get("hits", [])
    if hits:
        return hits[0]["result"]
    else:
        return None

# Function to scrape lyrics from Genius
def scrape_lyrics(song_url):
    page_response = requests.get(song_url)
    page_response.encoding = 'utf-8'  # Ensure proper character handling
    page_response.raise_for_status()
    html_content = BeautifulSoup(page_response.text, "html.parser")
    
    # Extract lyrics
    lyrics_divs = html_content.find_all("div", attrs={"data-lyrics-container": "true"})
    lyrics = "\n".join(html.unescape(div.get_text(separator="\n").strip()) for div in lyrics_divs)  # Decode HTML entities
    
    return lyrics if lyrics else None

# Initialize list for storing lyrics
lyrics_list = []

# Loop through songs, fetch lyrics, and append to list
for song_title, artist_name in songs_list:
    print(f"Processing: {song_title} by {artist_name}...")
    song_info = search_song(song_title, artist_name)
    
    if song_info:
        song_url = song_info.get("url")
        lyrics = scrape_lyrics(song_url)
        
        if lyrics:
            lyrics_list.append([lyrics])  # Only storing lyrics
            print(f"✅ Lyrics saved for {song_title}\n")
        else:
            print(f"❌ Could not extract lyrics for {song_title}\n")
    else:
        print(f"❌ Song not found: {song_title}\n")
    
    time.sleep(2)  # To prevent hitting API rate limits

# Convert to DataFrame and save to CSV (only lyrics)
df = pd.DataFrame(lyrics_list, columns=["Lyrics"])
print(df)

# Save as UTF-8-SIG to preserve special characters in Excel
df.to_csv(r"C:\Users\Student\OneDrive\Documents\atlanta.csv", index=False, encoding="utf-8-sig")

print("✅ All lyrics saved to atlanta_lyrics2.csv")
