#main.py
from flask import Flask, request, render_template, session, redirect
import pandas as pd

#add dash components
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input,Output

#import scrape function
import scrape

df = scrape.scrape()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Flask(__name__)


#dash app
dash_app = dash.Dash(
    __name__,
    server=app,
    routes_pathname_prefix='/dash/',
    external_stylesheets=external_stylesheets
)

dash_app.layout = html.Div(
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
    dash_table.DataTable(id='table',
    columns=[{"name":i,"id":i} for i in df.columns]
    )
    ]
)

@dash_app.callback(
    Output('table','data'),
    [Input('year-slider','value')]
)
def update_df(input_year):
    filtered_df = df[df.year==input_year].sort_values(by='imdb_ratings',ascending=False)
    filtered_data = filtered_df.to_dict('records')
    return filtered_data

#scraped dataframe
@app.route('/raw/')  
def home():
    return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

#main page
@app.route('/')
def main() :
    return "Welcome to my Internet Movies DashBoard "
    
if __name__ == '__main__':
    dash_app.run_server()
