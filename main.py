#main.py

import requests
from flask import Flask, request, render_template, session, redirect
import pandas as pd 
from bs4 import BeautifulSoup
import numpy as np
import re

app = Flask(__name__)

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

            metascore_= movie.find('span',class_='metascore').text if movie.find('span',class_='metascore') else '-'
            metascore.append(metascore_)

            vote = movie.find_all('span',attrs={'name':'nv'})[0].text
            votes.append(vote)

        df = pd.DataFrame({
            'movie':titles,
            'year':years,
            'imdb_ratings':imdb_ratings,
            'metacritic': metascore,
            'runtime':time,
            'votes':votes
        })

        df['year']=df['year'].apply(lambda x:re.findall(r"[0-9]+",x)[0])
        df['runtime']=df['runtime'].apply(lambda x:re.findall(r"[0-9]+",x)[0] )
        df['votes']=df['votes'].str.replace(',','').astype('int64')
        dfm = dfm.append(df)
        start += 50
    dfm.reset_index(drop=True,inplace=True)

    return dfm

@app.route('/raw')  
def home():
    return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/')
def main() :
    return "Welcome to Flask "

if __name__ == '__main__':
    df = scrape()
    app.run()
