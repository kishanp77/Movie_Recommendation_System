# -*- coding: utf-8 -*-
"""Movie_Recommendation_System.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w6JmxQ9rXMBh5TLq4dpCd7YB0IFJEPSe
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import pandas as pd

movies_df = pd.read_csv("/content/movies.xls")
movies_df.head(10)

ratings_df = pd.read_csv("/content/ratings.xls")
print("Movies:", movies_df.shape)
print("Ratings:", ratings_df.shape)
ratings_df.head(10)

tags_df = pd.read_csv("/content/tags.xls")
tags_df.head(10)

df = movies_df.merge(ratings_df, on = "movieId")
df.tail(20)

T_s = 'Toy Story (1995)' # title as input- it is just one movie
recommended_movies = []

## Find the movie in the database, and sort it byy rating
movie_db = df[df['title'] == T_s]\
           .sort_values(by = 'rating', ascending = False)

## First five users who liked this movie
for user in movie_db.iloc[:5]['userId'].values:

    ## getting the rated movies for this user
    rated_movies = df[df['userId'] == user]

    ## getting the five biggest rated movie by this user
    rated_movies = rated_movies[rated_movies['title'] != T_s]\
                    .sort_values(by = 'rating', ascending = False)\
                    .iloc[:5]

    ## adding these to recommendation
    recommended_movies.extend(list(rated_movies['title'].values))

recommended_movies = np.unique(recommended_movies)

for movie in recommended_movies:
    print(movie)

"""#### now weight each movie by the similarity on the genre feature:"""

gmovie_genres = df[df['title'] == T_s].iloc[0]['genres'].split('|')
scores = {}  ## {title: score ...}

for movie in recommended_movies:
   movied = df[df['title'] == movie].iloc[0]
   movie_genres = movied['genres'].split('|')
   score = 0

   # Scoring on how many gmovie_genre can be found in movie_genres
   for gmovie_genre in gmovie_genres:
    if gmovie_genre in movie_genres:
      score += 1

   scores[movie] = score


## sort them on score and reverse it, becouse the bigger the score the better
recommended_movies = sorted(scores, key = lambda x: scores[x])[::-1]

for movie in recommended_movies:
  print(movie)