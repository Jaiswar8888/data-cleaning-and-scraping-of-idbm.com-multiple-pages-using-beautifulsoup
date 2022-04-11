import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from time import sleep
from random import randint
import numpy as np

headers = dict()
headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"

titles = []
years = []
time = []
imdb_ratings = []
genre = []
votes = []
pages = np.arange(1, 1001, 50)
for page in pages:
    url = "https://www.imdb.com/search/title/?groups=top_1000&start=" + str(page)
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, "html.parser")
    movie_div = soup.find_all("div", class_="lister-item mode-advanced")
    sleep(randint(2, 10))
    print(page)
    for movieSection in movie_div:
        name = movieSection.h3.a.text
        titles.append(name)
        year = movieSection.h3.find("span", class_="lister-item-year").text
        years.append(year)
        ratings = movieSection.strong.text
        imdb_ratings.append(ratings)
        category = movieSection.find("span", class_="genre").text.strip()
        genre.append(category)
        runTime = movieSection.find("span", class_="runtime").text
        time.append(runTime)
        nv = movieSection.find_all("span", attrs={"name": "nv"})
        vote = nv[0].text
        votes.append(vote)
movies = pd.DataFrame(
    {
        "Movie": titles,
        "Year": years,
        "RunTime": time,
        "imdb": imdb_ratings,
        "Genre": genre,
        "votes": votes,
    }
)

# cleaning
movies["Year"] = movies["Year"].str.extract("(\\d+)").astype(int)
movies["RunTime"] = movies["RunTime"].str.replace("min", "minutes")
movies["votes"] = movies["votes"].str.replace(",", "").astype(int)

print(movies)
movies.to_csv(r"movies.csv", index=False, header=True)