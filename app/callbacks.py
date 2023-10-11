
from dash import Dash, html, dcc, callback, Output, Input, State, ALL, MATCH, ctx, dash_table

import pandas as pd
import io
import base64

import datetime

def make_callbacks(app):

    @app.callback(
            [
                Output(component_id='steps-output',component_property='children')
            ],
            [
                Input(component_id='step-add',component_property='n_clicks'),
                Input(component_id={'type': 'delete-button', 'index': ALL},
                    component_property='n_clicks'),
            ],
            [   
                State(component_id='steps-output',component_property='children'),
            ]
    )
    def add_step(n_clicks,
                delete_click,
                step_children):

        trigger = ctx.triggered_id if not None else 'No deletes yet'
        if (trigger=='step-add'):
            item = html.Div(
                        id = {'type':'step','index':n_clicks},
                        children = [
                            html.H3(f"Soon..{n_clicks}"),
                            dcc.Dropdown(
                                options=['Data Load','Preprocessing'],
                                value='Data Load',
                                id={'type':'step-type','index':n_clicks}
                            ),
                            html.Div(
                                id={'type':'step-selections','index':n_clicks}
                            ),
                            html.Button('X',id={'type':'delete-button','index':n_clicks})
                            ]
                    )
            step_children.append(
                    item
                )
            return [
                step_children
            ]
        else:
            idx = trigger.get('index')
            new_children = [
                i for i in step_children if i['props']['id']['index']!=idx
            ]
            return [
                new_children
            ]
        
    @app.callback(
            [
                Output(component_id={'type':'step-selections','index':MATCH},component_property='children'),
            ],
            [
                Input(component_id={'type':'step-type','index':MATCH},component_property='value'),
            ]
    )
    def define_step(step_type):

        trigger = ctx.triggered_id if not None else 'No deletes yet'

        if step_type=='Data Load':

            options = html.Div(
                id={'type':'data-load-options','index':trigger['index']},
                children=[
                    html.H5("This is a Data Load Step"),
                    dcc.Upload(
                        id={'type':'upload-data','index':trigger['index']},
                        children=html.Div(
                            children = [
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]
                        ),
                        multiple=False,
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                    ),
                    html.Div(
                        id={'type':'file-preview','index':trigger['index']}
                    )
                ]
            )
            return [
                options
            ]
        elif step_type=='Preprocessing':
            
            options = html.Div(
                id={'type':'preprocessing-options','index':trigger['index']},
                children=[
                    html.H5("This is a Preprocessing Step"),
                    dcc.Dropdown(
                        options=[
                            'VarianceThreshold'
                        ],
                        value='VarianceThreshold',
                        id={'type':'preprocessing-input','index':trigger['index']}
                        ),
                ]
            )

            return [
                options
            ]
    
    def parse_contents(contents, filename, date):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

        return html.Div([
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),

            dash_table.DataTable(
                df.head(10).to_dict('records'),
                [{'name': i, 'id': i} for i in df.columns]
            ),

            html.Hr(),  # horizontal line

            # For debugging, display the raw contents provided by the web browser
            html.Div('Raw Content'),
            html.Pre(contents[0:200] + '...', style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all'
            })
        ])


    @callback(
        [
            Output({'type':'file-preview','index':MATCH}, 'children'),
        ],
        [
            Input({'type':'upload-data','index':MATCH}, 'contents'),
        ],
        [
            State({'type':'upload-data','index':MATCH}, 'filename'),
            State({'type':'upload-data','index':MATCH}, 'last_modified')
        ]
    )
    def update_output(content, name, date):
        if content is not None:
            children = [
                parse_contents(content, name, date)
                ]
            return children
        else:
            return [
                html.H3('Waiting...')
            ]