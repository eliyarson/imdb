#main.py
from flask import Flask, request, render_template, session, redirect
import pandas as pd

#add dash components
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_functions

#import scrape function
import scrape

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Flask(__name__)
df = scrape.scrape()

#dash app
dash_app = dash.Dash(
    __name__,
    server=app,
    routes_pathname_prefix='/dash/',
    external_stylesheets=external_stylesheets
)

dash_app.layout = html.Div(
    [
    html.H4(children='Top 100 Movies'),
    dash_functions.generate_table(df,100)
    ]
)

#scraped dataframe
@app.route('/raw/')  
def home():
    return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

#main page
@app.route('/')
def main() :
    return "Welcome to Flask "
    
if __name__ == '__main__':
    dash_app.run_server()
