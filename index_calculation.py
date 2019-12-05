import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import json
import pandas as pd
from sqlalchemy import create_engine
import dash_table

#engine = create_engine('postgresql://elalbeiro:9988776655@extendedcase4.csuiz4fdxyvv.us-east-2.rds.amazonaws.com/postgres')
engine = create_engine('postgresql://nps_demo_user:nps_demo_user@ds4a-db.cfpdqvxu6j5d.us-east-2.rds.amazonaws.com/nps_demo_db')
barrios = pd.read_sql('select cod_barrio, barrio, index from barrios',engine.connect())
barrios_top = barrios.nlargest(15,'index')

token = 'pk.eyJ1IjoibmV3dXNlcmZvcmV2ZXIiLCJhIjoiY2o2M3d1dTZiMGZobzMzbnp2Z2NiN3lmdyJ9.cQFKe3F3ovbfxTsM9E0ZSQ'

def content():
	
	
	
	

	
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
			html.Div([
				html.Table([
					html.Tr([
						html.Td(
							html.Div([
								html.H3('Tabla de barrios'),
								dash_table.DataTable(
									id='table-neigs',
									columns=[{"name": i, "id": i} for i in barrios.columns],
									data=barrios.to_dict('records'),
									sort_action="native", 
									page_action="native",
									page_current= 0,
									page_size= 20
								),
							]), 
							style={'width': 400}
						),
						html.Td(
							html.Div([
								html.H3('Mapa'),
								dcc.Checklist(
									options=[
										{'label': 'Ver en mapa', 'value': 'MAP'}
									],
									value=[], 
									id='show-index-check'
								), 
								html.Br(),
								html.Div(id='index-map-content')
							]), 
							style={'width': 500}
						),
						html.Td(
							html.Div([
								html.H3('Boxplot'),
								dcc.Checklist(
									options=[
										{'label': 'Ver boxplot', 'value': 'BOX'}
									],
									value=[], 
									id='show-box-check'
								), 
								html.Br(),
								html.Div(id='index-boxplot-content'), 
								dcc.Graph(
									id='graph-2-tabs',
									figure={
										'data': [go.Box(
													y=barrios['index']
												)]
									}
								)
							]), 
							style={'width': 300}
						)
					])
				]),
			]),			
			html.Br(),
			html.Br(),
			html.Br(),
    ])
	
	
def update_index_map():

	with open('neigh_id.geojson') as f:
		geojson = json.loads(f.read())

	return html.Div([
				dcc.Graph(
					id = 'bogota-index-map', 
					figure={ 
							'data': [go.Choroplethmapbox(
								geojson=geojson,
								locations=barrios['cod_barrio'],
								text=barrios['barrio'],
								z=barrios['index'],
								colorscale='YlOrRd',
								colorbar_title="Values"
							)],
							'layout': go.Layout(
									mapbox_style="light",
									mapbox_accesstoken=token,
									mapbox_zoom=9,
									mapbox_center = {"lat": 4.6918154, "lon": -74.0765448}
							)
					}
				)
		])