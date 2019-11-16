import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import json
import pandas as pd

def content():
	return html.Div([
            html.H3('Tab content 2'),
            dcc.Dropdown(
					options=[
						{'label': 'New York City', 'value': 'NYC'},
						{'label': 'Montréal', 'value': 'MTL'},
						{'label': 'San Francisco', 'value': 'SF'}
					],
					value='MTL'
				),  
			dcc.Dropdown(
					options=[
						{'label': 'New York City', 'value': 'NYC'},
						{'label': 'Montréal', 'value': 'MTL'},
						{'label': 'San Francisco', 'value': 'SF'}
					],
					value='MTL'
				), 				
			dcc.Graph(
                    id='example-graph-3',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [2, 4, 3],
                                'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [5, 4, 3],
                             'type': 'bar', 'name': u'Montréal'},
                        ]
                    }
            )
        ])