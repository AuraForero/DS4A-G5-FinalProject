import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import json
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://elalbeiro:9988776655@extendedcase4.csuiz4fdxyvv.us-east-2.rds.amazonaws.com/postgres')

barrios = pd.read_sql('select cod_barrio, barrio from barrios',engine.connect())

barrios['cod_nombre_barrio'] = barrios['cod_barrio'] + ' ' + barrios['barrio']
barrios_data = list(barrios['cod_nombre_barrio'])


def content():
	return html.Div([
            html.H6('Seleccione un barrio'),
			dcc.Dropdown(
					id='barrios-dropdown',
					options=[{'label':barrio, 'value':barrio} for barrio in barrios_data]
			),
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