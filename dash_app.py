import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input,Output
import pandas as pd 
#import scrape function
import scrape
import numpy as np

#scraped dataframe
df = scrape.scrape()
genre_list = df.genres.str.split(",",expand=True)[0].append(df.genres.str.split(",",expand=True)[1]).append(df.genres.str.split(",",expand=True)[2]).dropna().str.strip().sort_values().unique()

#dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    requests_pathname_prefix='/dash/'
)

app.layout = html.Div(
    [
    html.H4(children='Top 1000 Movies'),
    html.Label('Slider'),
    dcc.Slider(
        id='year-slider',
        min=df.year.min(),
        max=df.year.max(),
        marks={i: 'Year {}'.format(i) if i == df.year.min() else str(i) for i in range(df.year.min(), df.year.max()+1,10)},
        value=2019
    ),
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label':i,'value':''} if i=='All' else {'label':i,'value':i} for i in genre_list],
        value=''
    ),
    dash_table.DataTable(id='table',
    columns=[{"name":i,"id":i} for i in df.columns],
    sort_action='native',
    sort_mode='multi'
    )
    ]
)

@app.callback(
    Output('table','data'),
    [Input('year-slider','value'),
    Input ('genre-dropdown','value')]
)
def update_df(input_year,input_genre):
    filtered_df = df[df.year==input_year].sort_values(by='imdb_ratings',ascending=False)
    if input_genre == None:
        filtered_df = filtered_df[filtered_df.genres.str.contains('')]
    else:
        filtered_df = filtered_df[filtered_df.genres.str.contains(input_genre)]
    filtered_data = filtered_df.to_dict('records')
    return filtered_data