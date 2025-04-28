# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 11:35:43 2025

@author: Student
"""


import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import os
import re


# Set the directory (change based on your computer's directory)
os.chdir(r"C:\Users\Student\OneDrive\Desktop\prototyping\lyrics")

# Load CSV files
files = ["LA_clean.csv", "NYC_clean.csv", "atlanta_clean.csv", "chicago_clean.csv", 
         "miami_clean.csv", "DC_clean.csv", "houston_clean.csv"]
cities = ["LA", "NYC", "Atlanta", "Chicago", "Miami", "DC", "Houston"]

# Read and preprocess files
corpus = []
for file in files:
    df = pd.read_csv(file, dtype=str)
    text = " ".join(df.astype(str).values.flatten())  # Flatten and join all text
    text = re.sub(r"\b(verse|chorus|lyrics)\b", "", text, flags=re.IGNORECASE)  # Remove unwanted words
    corpus.append(text)

# Apply TF-IDF
#Decided to remove the "stop words", this is uses a built in function to TfidfVectorizer to remove common
#english words like "the", "and", "as"
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(corpus)

# Convert to DataFrame for readability
tfidf_df = pd.DataFrame(X.toarray(), index=cities, columns=vectorizer.get_feature_names_out())

# Display top 10 words for each city
for city in cities:
    print(f"Top TF-IDF words for {city}:")
    print(tfidf_df.loc[city].sort_values(ascending=False).head(10))
    print("\n" + "="*50 + "\n")
