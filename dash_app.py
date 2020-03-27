import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import numpy as np

#scraped dataframe
df = pd.read_csv('data.csv')

genre_list = df.genres.str.split(",", expand=True)[0].append(df.genres.str.split(",", expand=True)[
    1]).append(df.genres.str.split(",", expand=True)[2]).dropna().str.strip().sort_values().unique()

#dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    requests_pathname_prefix='/dash/'
)

app.layout = html.Div(
    [
        #Header
        html.H1(children='Top 1000 Movies'),
        html.Div([
            html.Label('Slider'),
            dcc.Slider(
                id='year-slider',
                min=df.year.min(),
                max=df.year.max(),
                marks={i: 'Year {}'.format(i) if i == df.year.min() else str(
                    i) for i in range(df.year.min(), df.year.max()+1, 10)},
                value=2019
            )]),
        html.Div([
            dcc.Dropdown(
                id='genre-dropdown',
                options=[{'label': i, 'value': ''} if i == 'All' else {
                    'label': i, 'value': i} for i in genre_list],
                value=''
            )]),
        html.Div([
            dcc.Graph(
                id='movie-graph'
            )
        ]),
        html.Div([
            dash_table.DataTable(id='table',
                                 columns=[{"name": i, "id": i}
                                          for i in df.columns],
                                 sort_action='native',
                                 sort_mode='multi'
                                 )
            ])
    ], style={'columnCount': 1,
              'width': '95%'})


@app.callback(
    [Output('table', 'data'),
    Output('movie-graph','figure')],
    [Input('year-slider', 'value'),
     Input('genre-dropdown', 'value')]
)
def update_df(input_year, input_genre):
    filtered_df = df[df.year == input_year].sort_values(
        by='imdb_ratings', ascending=False)
    if input_genre == None:
        filtered_df = filtered_df[filtered_df.genres.str.contains('')]
    else:
        filtered_df = filtered_df[filtered_df.genres.str.contains(input_genre)]

    filtered_data = filtered_df.to_dict('records')
    figure = {'data':[
        {
        'x': filtered_df['metacritic'],
        'y': filtered_df['imdb_ratings'],
        'text': filtered_df['movie'],
        'mode':'markers'
        }
        ]}
    
    return filtered_data,figure

