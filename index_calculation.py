import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import json
import pandas as pd
from sqlalchemy import create_engine
import dash_table
import numpy as np

engine = create_engine('postgresql://elalbeiro:9988776655@extendedcase4.csuiz4fdxyvv.us-east-2.rds.amazonaws.com/postgres')

token = 'pk.eyJ1IjoibmV3dXNlcmZvcmV2ZXIiLCJhIjoiY2o2M3d1dTZiMGZobzMzbnp2Z2NiN3lmdyJ9.cQFKe3F3ovbfxTsM9E0ZSQ'

def content():

	# engine = create_engine('postgresql://nps_demo_user:nps_demo_user@ds4a-db.cfpdqvxu6j5d.us-east-2.rds.amazonaws.com/nps_demo_db')
	barrios = pd.read_sql('select cod_barrio,  barrio, c1_index AS index, cluster from info_barrios_codigos_1',
						  engine.connect())
	barrios_top = barrios.nlargest(15, 'index')

	x_df = pd.read_csv('data/x_df.csv')
	centers_df = pd.read_csv('data/centers_df.csv')

	with open('neigh_id.geojson') as f:
		geojson = json.loads(f.read())
	
	return html.Div([
			html.Div(
				className="row",
				children=[
					html.Div([
						html.Br(),
						html.H5("Distribución geografica del indice", className='my-subtitles' ),
						dcc.Graph(
							id = 'bogota-index-map', 
							figure={ 
								'data': [
											go.Choroplethmapbox(
												geojson=geojson,
												locations=barrios['cod_barrio'],
												text=barrios['barrio'],
												z=barrios['index'],
												colorscale='YlOrRd',
												colorbar_title="Indices"
										)],
								'layout': go.Layout(
											mapbox_style="light",
											mapbox_accesstoken=token,
											mapbox_zoom=10,
											mapbox_center = {"lat": 4.6418154, "lon": -74.0765448}
										)
							}
						),
						html.Div(id='index-map-content')
					])
				]	
			),
			html.Div(
				className="row",
                children=[
					html.Br(),
					html.Div(
						id='div-boxplot-index', 
						className="six columns",
						children=[
							html.H5('Distribución global del indice', className='my-subtitles'),
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
										go.Scatter(x=x_df['0'], 
													y=x_df['1'], 
													mode='markers',
													marker_color=x_df['y_kmeans'],	
													name='Clusters', 
													marker=dict(
														size=10,
														color=np.random.randn(500), #set color equal to a variable
														colorscale='Viridis', # one of plotly colorscales
														showscale=True
													), 
													text=barrios['barrio']
										), 
										go.Scatter(x=centers_df['0'], 
													y=centers_df['1'], 
													mode='markers',
													name='Centros', 
													marker_color='black'
										)
									]
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
					html.Div([
						html.Br(),
						html.H5('Distribución geografica de los clusteres', className='my-subtitles'),
						dcc.Graph(
							id = 'bogota-cluster-map', 
							figure={ 
								'data': [
											go.Choroplethmapbox(
												geojson=geojson,
												locations=barrios['cod_barrio'],
												text=barrios['barrio'],
												z=barrios['cluster'],
												colorscale='YlGnBu',
												colorbar_title="Clusters"
										)],
								'layout': go.Layout(
											mapbox_style="light",
											mapbox_accesstoken=token,
											mapbox_zoom=10,
											mapbox_center = {"lat": 4.6418154, "lon": -74.0765448}
										)
							}
						),
						html.Div(id='index-map-content')
					])
				]	
			),
			html.Div(
				className="row",
                children=[
					html.H5('Barrios con mejor indice', className='my-subtitles'),
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
						html.H5('Tabla de barrios', className='my-subtitles'),
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
				]
			),
		])
	
	
def update_index_map():

	engine = create_engine(
		'postgresql://elalbeiro:9988776655@extendedcase4.csuiz4fdxyvv.us-east-2.rds.amazonaws.com/postgres')
	# engine = create_engine('postgresql://nps_demo_user:nps_demo_user@ds4a-db.cfpdqvxu6j5d.us-east-2.rds.amazonaws.com/nps_demo_db')
	barrios = pd.read_sql('select cod_barrio,  barrio, c1_index AS index, cluster from info_barrios_codigos_1',
						  engine.connect())

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
	engine = create_engine(
		'postgresql://elalbeiro:9988776655@extendedcase4.csuiz4fdxyvv.us-east-2.rds.amazonaws.com/postgres')
	# engine = create_engine('postgresql://nps_demo_user:nps_demo_user@ds4a-db.cfpdqvxu6j5d.us-east-2.rds.amazonaws.com/nps_demo_db')
	barrios = pd.read_sql('select cod_barrio,  barrio, c1_index AS index, cluster from info_barrios_codigos_1',
						  engine.connect())

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
	engine = create_engine(
		'postgresql://elalbeiro:9988776655@extendedcase4.csuiz4fdxyvv.us-east-2.rds.amazonaws.com/postgres')
	# engine = create_engine('postgresql://nps_demo_user:nps_demo_user@ds4a-db.cfpdqvxu6j5d.us-east-2.rds.amazonaws.com/nps_demo_db')
	barrios = pd.read_sql('select cod_barrio,  barrio, c1_index AS index, cluster from info_barrios_codigos_1',
						  engine.connect())

	return 	{
			'data': [go.Box(
						y=barrios['index'], 
						name='Indice', 
						boxpoints='suspectedoutliers'
					)
					]
		}
		
def update_elbow():
	engine = create_engine(
		'postgresql://elalbeiro:9988776655@extendedcase4.csuiz4fdxyvv.us-east-2.rds.amazonaws.com/postgres')
	# engine = create_engine('postgresql://nps_demo_user:nps_demo_user@ds4a-db.cfpdqvxu6j5d.us-east-2.rds.amazonaws.com/nps_demo_db')
	barrios = pd.read_sql('select cod_barrio,  barrio, c1_index AS index, cluster from info_barrios_codigos_1',
						  engine.connect())

	elbow_df = pd.read_csv('data/elbow_plot_data.csv')

	return 	dcc.Graph(
					id='graph-elbow',
						figure={
							'data': [
								go.Scatter(x=elbow_df['NumberClusters'], y=elbow_df['Score']
						)]
					}
				)