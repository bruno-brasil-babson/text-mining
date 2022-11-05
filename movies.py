### DATA PROCESSING SCRIPT ###

from imdb import Cinemagoer
import pickle
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd 

from sqlalchemy import true

## PROMPT - Sentiment analysis in utopia and dystopias
# movie attributes: genres, plot, synopsis, rating
# 1. categorization of utopia/dystopias across genres
# 2. most common words in plot & synopsis
# 3. plot & synopsis sentiment analysis (summary stats)

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

# print("Utopia genres are:")
# print(genre_freq(utopia_IDs))
# print("Dystopia genres are:")
# print(genre_freq(dystopia_IDs))


## 2. For both utopia and dystopia, create a function that, for a list of movie id's,
# return a dict of words:(frequency of words in movies' plot), and other to
# return a dict of words:(frequency of words in movies' synopsis),
# both sorted by values -> we want top50 in each to compare

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
    print("\n")
    return True

def intersect_first(l1, l2, n):
    """
    returns the intersection of two lists of tuples for their first elements
    """
    s1 = []
    s2 = []
    for i in range(n):
        s1.append(l1[i][0])
        s2.append(l2[i][0])
    return list(set(s1) & set(s2))
        

# wf_utopia_plots = word_freq('data/utopia_plots.txt')
# wf_dystopia_plots = word_freq('data/dystopia_plots.txt')
# # top(wf_utopia_plots, 50)
# # top(wf_dystopia_plots, 50)
# wf_utopia_synopsis = word_freq('data/utopia_synopsis.txt')
# wf_dystopia_synopsis = word_freq('data/dystopia_synopsis.txt')

# print(intersect_first(wf_utopia_plots, wf_dystopia_plots, 50))
# print(intersect_first(wf_utopia_synopsis, wf_dystopia_synopsis, 50))

## 3. For both utopia and dystopia, create a function that, for a list of movie id's,
# return summary statistics for each movie's plot and synopsis

def sentiment_scores(filename):
    """
    for a list of texts, return a list of their sentiment analysis score 
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

# utopia_plot_scores = sentiment_scores('data/utopia_plots.txt')
# dystopia_plot_scores = sentiment_scores('data/dystopia_plots.txt')
# print("Utopia plots (summary stats)")
# print(summary_stats(utopia_plot_scores))
# print("Dystopia plots (summary stats)")
# print(summary_stats(dystopia_plot_scores))

# utopia_synopsis_scores = sentiment_scores('data/utopia_synopsis.txt')
# dystopia_synopsis_scores = sentiment_scores('data/dystopia_synopsis.txt')
# print("Utopia synopsis (summary stats)")
# print(summary_stats(utopia_synopsis_scores))
# print("Dystopia synopsis (summary stats)")
# print(summary_stats(dystopia_synopsis_scores))


def main():
    # 1. Genre frequency in utopia and dystopia's movies
    print("Utopia genres are:")
    print(genre_freq(utopia_IDs))
    print("Dystopia genres are:")
    print(genre_freq(dystopia_IDs))

    # 2. Plot and synopsis intersection word analysis
    wf_utopia_plots = word_freq('data/utopia_plots.txt')
    wf_dystopia_plots = word_freq('data/dystopia_plots.txt')
    wf_utopia_synopsis = word_freq('data/utopia_synopsis.txt')
    wf_dystopia_synopsis = word_freq('data/dystopia_synopsis.txt')
    print(intersect_first(wf_utopia_plots, wf_dystopia_plots, 50))
    print(intersect_first(wf_utopia_synopsis, wf_dystopia_synopsis, 50))

    # 3. Summary statistics of plot and synopsis sentiment analysis
    utopia_plot_scores = sentiment_scores('data/utopia_plots.txt')
    dystopia_plot_scores = sentiment_scores('data/dystopia_plots.txt')
    print("Utopia plots (summary stats)")
    print(summary_stats(utopia_plot_scores))
    print("Dystopia plots (summary stats)")
    print(summary_stats(dystopia_plot_scores))

    utopia_synopsis_scores = sentiment_scores('data/utopia_synopsis.txt')
    dystopia_synopsis_scores = sentiment_scores('data/dystopia_synopsis.txt')
    print("Utopia synopsis (summary stats)")
    print(summary_stats(utopia_synopsis_scores))
    print("Dystopia synopsis (summary stats)")
    print(summary_stats(dystopia_synopsis_scores))

if __name__ == '__main__':
    main()