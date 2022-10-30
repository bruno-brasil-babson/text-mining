### DATA PROCESSING SCRIPT ###

from imdb import Cinemagoer
import pickle
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd 

from sqlalchemy import true

## PROMPT - Sentiment analysis in utopia and dystopias
# movie attributes: genres (freq.), plot, synopsis, rating, votes ()
# 1. categorization of utopia/dystopias across genres
# 2. most common words in plot & synopsis
# 3. does movie with good ratings have more intense plot & synopsis (sentiment analysis)

with open('data/utopia.pickle', 'rb') as input_file:
    utopia_IDs = pickle.load(input_file)

with open('data/dystopia.pickle', 'rb') as input_file:
    dystopia_IDs = pickle.load(input_file)

# create an instance of the Cinemagoer class
ia = Cinemagoer()

## 0. Print list of movie titles

with open('data/utopia_titles.pickle', 'rb') as input_file:
    utopia_titles = pickle.load(input_file)

with open('data/dystopia_titles.pickle', 'rb') as input_file:
    dystopia_titles = pickle.load(input_file)

# Which movies are in each category?
# print(utopia_titles)
# print(dystopia_titles)

def intersect(l1, l2, n):
    """
    returns the intersection of two lists' N first elements
    """
    s1 = []
    s2 = []
    for i in range(n):
        s1.append(l1[i])
        s2.append(l2[i])
    return list(set(s1) & set(s2))
    
# Only 3 movies in both "categories". Check below:
# print(intersect(utopia_titles, dystopia_titles, 50))

## 1. Genre frequency in utopia and dystopia's movies

def genre_freq(ids):
    """
    input: list of movie IDs
    output: dict of genres:(number of movies from the list with this genre) sorted by values
    """
    d = {}
    for id in ids:
        m = ia.get_movie(id)
        genres = m.get('genres')
        for g in genres:
            if g not in d.keys():
                d[g] = 1
            else:
                d[g] += 1

    sort_genres = sorted(d.items(), key = lambda x:x[1], reverse = True)
    return sort_genres

# print("Utopia genres are:", genre_freq(utopia_IDs))
# print("Dystopia genres are:", genre_freq(dystopia_IDs))


## 2. For both utopia and dystopia, create a function that, for a list of movie id's,
# return a dict of words:(frequency of words in movies' plot), and other to
# return a dict of words:(frequency of words in movies' synopsis),
# both sorted by values -> we want top100 in each to compare

def word_freq(filename):
    """
    opens file and returns a dict with words:(word frequency in file)
    """
    d = {}
    fp = open(filename)

    strippables = string.punctuation + string.whitespace

    for line in fp:
        line = line.replace('-', ' ')
        line = line.replace('[', ' ')
        line = line.replace(']', ' ')
        line = line.replace('/', ' ')
        line = line.replace('::', ' ')

        for word in line.split():
            word = word.strip(strippables)
            word = word.lower()

            d[word] = d.get(word, 0) + 1

    sort_words = sorted(d.items(), key = lambda x:x[1], reverse = True)
    return sort_words

def top(l, n):
    """
    prints the first n elements of a list
    """
    for i in range(n):
        print(l[i])
    return True

def intersect_first(l1, l2, n):
    """
    returns the intersection of two lists' N first pairs
    """
    s1 = []
    s2 = []
    for i in range(n):
        s1.append(l1[i][0])
        s2.append(l2[i][0])
    return list(set(s1) & set(s2))
        

# wf_utopia = word_freq('data/utopia_plots.txt')
# wf_dystopia = word_freq('data/dystopia_plots.txt')
# # top(wf_utopia, 50)
# # top(wf_dystopia, 50)
# print(intersect(wf_utopia, wf_dystopia, 100))

## 3. For both utopia and dystopia, create a function that, for a list of movie id's,
# return a list of tuples (rating, votes, sentiment['compound']) for each movie's plot

def plot_sentScore(filename):
    """
    for a list of plots, return a list of their sentiment analysis score 
    """
    fp = open(filename)
    score_list = []
    for line in fp:
        line = line.replace('[', ' ')
        line = line.replace(']', ' ')
        line = line.replace('::', ' ')

        score = SentimentIntensityAnalyzer().polarity_scores(line)
        score_list.append(score)
    return score_list

def summary_stats(scores):
    """
    for a list of sentiment analysis scores, returns summary stats
    """
    comp = []
    for score in scores:
        comp_score = score['compound']
        comp.append(comp_score)
    comp_series = pd.Series(comp)

    return comp_series.describe()

# print(plot_sentScore('data/utopia_plots.txt'))
# print(plot_sentScore('data/dystopia_plots.txt'))

utopia_scores = plot_sentScore('data/utopia_plots.txt')
dystopia_scores = plot_sentScore('data/dystopia_plots.txt')
# print(summary_stats(utopia_scores))
print(summary_stats(dystopia_scores))