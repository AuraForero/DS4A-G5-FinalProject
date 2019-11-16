import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import json
import pandas as pd

def content():
	return html.Div([
            html.H3('Tab content 3'),
            dcc.Graph(
                id='graph-3-tabs',
                figure={
                    'data': [{
                        'x': [6, 6, 1],
                        'y': [4, 3, 7],
                        'type': 'bar'
                    }]
                }
            )
        ])