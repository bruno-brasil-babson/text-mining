### DATA FETCHING SCRIPT ###

from imdb import Cinemagoer
import pickle

# create an instance of the Cinemagoer class
ia = Cinemagoer()

utopia = ia.get_keyword('utopia')
dystopia = ia.get_keyword('dystopia')

## 0. IDs ##
def id(movies):
    """
    for a list of movies, return a list of their movie IDs
    """
    movie_ids = []
    for i in range(len(movies)):
        id = movies[i].movieID
        movie_ids.append(id)
    return movie_ids

utopia_IDs = id(utopia)
dystopia_IDs = id(dystopia)

with open('data/utopia.pickle', 'wb') as f:
    pickle.dump(utopia_IDs, f)

with open('data/dystopia.pickle', 'wb') as f:
    pickle.dump(dystopia_IDs, f)

with open('data/utopia.pickle', 'rb') as input_file:
    utopia_IDs = pickle.load(input_file)

with open('data/dystopia.pickle', 'rb') as input_file:
    dystopia_IDs = pickle.load(input_file)

## 1. Titles ##

def titles(ids):
    """
    for a list of movie IDs, return a dict mapping ID:(movie titles)
    """
    titles = []
    for id in ids:
        m = ia.get_movie(id)
        title = m.get('title')
        titles.append(title)
    return titles

utopia_titles = titles(utopia_IDs)
dystopia_titles = titles(dystopia_IDs)

with open('data/utopia_titles.pickle', 'wb') as f:
    pickle.dump(utopia_titles, f)

with open('data/dystopia_titles.pickle', 'wb') as f:
    pickle.dump(dystopia_titles, f)

## 2. Plots ##

def plots(ids):
    """
    for a list of movie IDs, return a dict mapping ID:(movie plots)
    """
    d = {}
    for id in ids:
        m = ia.get_movie(id)
        d[id] = m.get('plot')
    return d

# utopia_plots = plots(utopia_IDs)
# dystopia_plots = plots(dystopia_IDs)

# with open('data/utopia_plots.txt', 'w') as f:
#     for plot in utopia_plots.values():
#         f.write("%s\n" % plot)
    
# with open('data/dystopia_plots.txt', 'w') as f:
#     for plot in dystopia_plots.values():
#         f.write("%s\n" % plot)

## 3. Synopsis ##

def synopsis(ids):
    """
    for a list of movie IDs, return a dict mapping ID:(movie synopsis)
    """
    d = {}
    for id in ids:
        m = ia.get_movie(id)
        d[id] = m.get('synopsis')
    return d

# utopia_synopsis = synopsis(utopia_IDs)
# dystopia_synopsis = synopsis(dystopia_IDs)

# with open('data/utopia_synopsis.txt', 'w') as f:
#     for synopsis in utopia_synopsis.values():
#         f.write("%s\n" % synopsis)
    
# with open('data/dystopia_synopsis.txt', 'w') as f:
#     for synopsis in dystopia_synopsis.values():
#         f.write("%s\n" % synopsis)