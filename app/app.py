
from dash import Dash, html, dcc, callback, Output, Input, State, ALL, MATCH, ctx
from flask import Flask

from callbacks import make_callbacks

from data_processing import (
    load_csv_data
)

def create_app(server):

    app = Dash(__name__,
               server=server,
               prevent_initial_callbacks=True
               )
    
    app.layout = html.Div(
        [
            html.H1("ClickLearn"),
            html.Button('+Add Step',id='step-add',n_clicks=0,),
            html.Div(id='steps-output',children=[
            ])
        ]
    )

    make_callbacks(app)
    

    return app

if __name__ == '__main__':

    server = Flask(__name__)
    app = create_app(server = server)
    
    app.run(debug=True)