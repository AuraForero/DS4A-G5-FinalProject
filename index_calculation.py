import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import json
import pandas as pd
from sqlalchemy import create_engine
import dash_table

def content():
	
	
	
	
	#engine = create_engine('postgresql://elalbeiro:9988776655@extendedcase4.csuiz4fdxyvv.us-east-2.rds.amazonaws.com/postgres')
	engine = create_engine('postgresql://nps_demo_user:nps_demo_user@ds4a-db.cfpdqvxu6j5d.us-east-2.rds.amazonaws.com/nps_demo_db')
	barrios = pd.read_sql('select * from barrios',engine.connect())
	barrios.drop(['level_0'], axis=1)
	barrios_top = barrios.nlargest(15,'index')
	
	return html.Div([
            html.H3('Barrios con mejor indice'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [go.Bar(
									x=barrios_top['barrio'], y=barrios_top['index']
							)]
                }
            ), 
			html.H3('Tabla de barrios'),
			dash_table.DataTable(
				id='table-neigs',
				columns=[{"name": i, "id": i} for i in barrios.columns],
				data=barrios.to_dict('records'),
				sort_action="native"
			), 
			html.Br(),
			html.Br(),
			html.Br(),
			dcc.Checklist(
				options=[
					{'label': 'Ver en mapa', 'value': 'MAP'}
				],
				value=[], 
				id='show-index-check'
				
			), 
			html.Br(),
			html.Div(id='index-map-content')	
			
    ])