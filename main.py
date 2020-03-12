#main.py
from flask import Flask, request, render_template, session, redirect
import pandas as pd

#add dash components
import dash
import dash_html_components as html


#import scrape function
import scrape

app = Flask(__name__)
df = scrape.scrape()

#dash app
dash_app = dash.Dash(
    __name__,
    server=app,
    routes_pathname_prefix='/dash/'
)

dash_app.layout = html.Div("My Dash app")

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
