# Analysis of Utopia & Dystopia Movies on IMDb

## Project Overview

In this project, I analyzed similarities and differences related to movies about utopias and/or dystopias. The motivation to that is my LTA class, which is about that them, and has shown me how thin the border between these ideas can be. The data source was the `cinemagoer` package, which provided a range of information about movies and allowed to query on my 2 chosen keywords. The study consisted of analysis across the two categories, be it genre frequency, most common words in the movies' plots and synopsis, and plots' sentiment analysis.

## Implementation

The project's code has two scripts: 
- `start.py` retrieves data from `cinemagoer` and save it in `data` folder
- `movies.py` runs analysis on data saved on `data` folder

I decided to save data beforehand because the package takes too long to retrieve the data. As the focus of the project was on analysis, the text analysis would be iterated much more than querying operations. So, when chosing if I should have all my code in just one script, I decided to prioritize iteration speed. Therefore, I split the code in two files based on two types of functions: *analysis* functions, and *querying* functions. The former constitute `movies.py`, while the latter are in `start.py` along with pickle dump processes. 

The data structures and file types to store data from the package were chosen based on the purpose of the data. For example, for the IDs of Utopia and Dystopia movies, I chose to pickle the list, as accessing the list would be much more important than visualizing it. On the other hand, to movies' plots and synopsis, I decided to save them as .txt files, as this are straightforward to read inside a function, while preserving text format so I could read the source data if I needed to. Similarly, synopsis were saved as txt.

In the analysis functions, I chose to use *dictionaries* as main data structure for frequencies. For example, in genre frequency, the dictionary maps genre to number of movies from the list of IDs with such genre. This allowed for a logical map between categorical data and counting appearences, and smooth sorting process by higher frequency.

Finally, I used Python `pandas` package to get summary statistics from a list of sentiment analysis scores. As the size of both sets were considerable (N = 50), just looking at scores was not enough to compare them. So pandas statistics could provide a quick view of numerical data from a list of scores from NLTK package for sentiment analysis.   

## Results

After doing keyword search for Utopia and Dystopia in IMDb movies and shows' dataset, we get 50 movies in each. First, I checked how many movies where in both. To my surprise, only 3: Watchmen, THX 1138, and Total Recall. 

When looking at genres frequency, we learn that 31 out of the 50 utopia movies are in the "Sci-Fi" category, yet, in dystopia they are 43! Indeed, if we look at the other top genres in dystopia, we can have an idea of what Hollywood values in distopian movies: "Sci-fi, Action, Thriller, Drama". On the other side, half (25) of utopian movies are in the "Adventure" genre, showing how utopic stories fit in a lighter spectrum than dystopic ones. Still, genres are mostly similar across these categories, highlighting once again common themes in these stories. 

For plots and synopsis, we take a look on which words appear the most. Recalling what they mean, plot is a short description of the main theme of the movie, while synopsis is a much more detailed version of the full story. The method chosen was to check the top 50 words in frequency among plots, and compare across categories, then later do the same for synopsis. 

**Common words in top 50 among utopia vs. dystopia plots (42)**
![plots_freq](images/plots_freq.jpg)
**Common words in top 50 among utopia vs. dystopia synopsis (47)**
![synopsis_freq](images/synopsis_freq.jpg)

## Reflection