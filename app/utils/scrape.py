import pandas as pd 
from bs4 import BeautifulSoup
import requests
import numpy as np
import re

def scrape():
    headers = {"Accept-Language":"en-US, en, q=0.5s"}
    start = 1
    dfm = pd.DataFrame()
    while start < 1000:
        url = "https://www.imdb.com/search/title/?groups=top_1000&start={0}&ref_=adv_nxt".format(start)
        results = requests.get(url, headers=headers)
        soup = BeautifulSoup(results.text,"html.parser")
        movies = soup.find_all('div',class_='lister-item mode-advanced')
        titles=[]
        years=[]
        time=[]
        imdb_ratings=[]
        metascore=[]
        votes=[]
        us_gross=[]
        genres = []
        for movie in movies:
            title=movie.h3.a.text
            titles.append(title)

            year = movie.find('span',class_='lister-item-year text-muted unbold').text
            years.append(year)

            runtime= movie.find('span',class_='runtime').text if movie.find('span',class_='runtime') else '-'
            time.append(runtime)

            imdb_rating = movie.find('div',class_='inline-block ratings-imdb-rating').strong.text
            imdb_ratings.append(imdb_rating)

            metascore_= movie.find('span',class_='metascore').text.strip() if movie.find('span',class_='metascore') else '-'
            metascore.append(metascore_)

            vote = movie.find_all('span',attrs={'name':'nv'})[0].text
            votes.append(vote)

            gross = movie.find_all('span',attrs={'name':'nv'})[1].text if len(movie.find_all('span',attrs={'name':'nv'}))>1 else '-'
            us_gross.append(gross)

            genre = movie.find('span',class_='genre').text
            genres.append(genre)

        df = pd.DataFrame({
            'movie':titles,
            'year':years,
            'imdb_ratings':imdb_ratings,
            'metacritic': metascore,
            'runtime':time,
            'votes':votes,
            'genres':genres,
            'us_gross':us_gross
        })

        df.year=df.year.apply(lambda x:re.findall(r"[0-9]+",x)[0]).astype(int)
        df['runtime']=df['runtime'].apply(lambda x:re.findall(r"[0-9]+",x)[0] )
        df['votes']=df['votes'].str.replace(',','').astype('int64')
        df.genres = df.genres.str.strip()
        dfm = dfm.append(df)
        start += 50
    dfm.reset_index(drop=True,inplace=True)

    dfm.to_csv('data.csv',index=False,sep=",")

scrape()
