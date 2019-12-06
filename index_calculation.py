import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import json
import pandas as pd
from sqlalchemy import create_engine
import dash_table
import numpy as np

engine = create_engine('postgresql://elalbeiro:9988776655@extendedcase4.csuiz4fdxyvv.us-east-2.rds.amazonaws.com/postgres')
#engine = create_engine('postgresql://nps_demo_user:nps_demo_user@ds4a-db.cfpdqvxu6j5d.us-east-2.rds.amazonaws.com/nps_demo_db')
barrios = pd.read_sql('select cod_barrio, barrio, index, cluster from barrios',engine.connect())
barrios_top = barrios.nlargest(15,'index')

x = np.arange(10)

token = 'pk.eyJ1IjoibmV3dXNlcmZvcmV2ZXIiLCJhIjoiY2o2M3d1dTZiMGZobzMzbnp2Z2NiN3lmdyJ9.cQFKe3F3ovbfxTsM9E0ZSQ'

def content():

	
	return html.Div([
			html.Div(
				className="row",
                children=[
					html.Br(),
					html.Div(
						id='div-boxplot-index', 
						className="six columns",
						children=[
							html.H5('Distribución global del indice'),
							dcc.Checklist(
									options=[
										{'label': 'Incluir media y desviacion estandar', 'value': 'SDBOX'}
									],
									value=[], 
									id='show-index-sd'
							),
							dcc.Graph(
								id='graph-boxplot-index',
								figure={
									'data': [go.Box(
													y=barrios['index'], 
													name='Indice', 
													boxpoints='suspectedoutliers'
												)
											]
								}
							)
						]	
					),
					html.Div(
						className="six columns",
						children=[
							html.H5('Agrupación con base en caracteristicas'),
							dcc.Graph(
								id='graph-2-tabs',
								figure={
									'data': [
										go.Scatter(x=barrios['index'], 
													y=barrios['cluster'], 
													mode='markers',
													marker_color=barrios['cluster'],													
													text=barrios['barrio']
									)]
								}
							),
							dcc.Checklist(
								options=[
									{'label': 'Ver gráfica de método Elbow', 'value': 'ELBOW'}
								],
								value=[], 
								id='show-elbow'
							), 
							html.Div(id='elbow-content')
						]	
					)
				]
			),
			html.Div(
				className="row",
                children=[
					html.H5('Barrios con mejor indice'),
							dcc.Graph(
								id='graph-2-tabs',
								figure={
									'data': [go.Bar(
										x=barrios_top['barrio'], y=barrios_top['index']
									)]
								}
					)
				]
			),
			html.Div(
				className="row",
				children=[
					html.Div(
						className="six columns",
						children=[
						html.H5('Tabla de barrios'),
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
					html.Div(
						className="six columns",
						children=[
							html.Div([
								html.H5('Heatmap del indice'),
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
						]	
					)
				]
			),
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
		
def update_boxplot_index_sd():	
		return 	{
			'data': [go.Box(
						y=barrios['index'], 
						name='Indice', 
						boxmean='sd',
						boxpoints='suspectedoutliers'
					)
					]
		}
					
def update_boxplot_index_no_sd():	
		return 	{
			'data': [go.Box(
						y=barrios['index'], 
						name='Indice', 
						boxpoints='suspectedoutliers'
					)
					]
		}
		
def update_elbow():	
		return 	dcc.Graph(
					id='graph-elbow',
						figure={
							'data': [
								go.Scatter(x=x, y=x**2
						)]
					}
				)