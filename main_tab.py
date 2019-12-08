import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import json
from barrios import app
import pandas as pd
from sqlalchemy import create_engine
import time



engine = create_engine('postgresql://elalbeiro:9988776655@extendedcase4.csuiz4fdxyvv.us-east-2.rds.amazonaws.com/postgres')
#engine = create_engine('postgresql://nps_demo_user:nps_demo_user@ds4a-db.cfpdqvxu6j5d.us-east-2.rds.amazonaws.com/nps_demo_db')
airbnb = pd.read_sql('select * from airbnb',engine.connect())
periods_data = airbnb.Fecha_Corte.unique()
periods_data.sort()
periods_data = list(periods_data)
airbnb_date = airbnb[airbnb['Fecha_Corte']=='2019-02-01']

airbnb_date.Media_Arriendo = airbnb_date.Media_Arriendo.astype(float)
data_to_map = airbnb_date[['Cod_Barrio','Barrio','Media_Arriendo']]
data_to_map.set_index('Cod_Barrio')
#data_to_map = data_to_map[data_to_map['Media_Arriendo'] > 0]


token = 'pk.eyJ1IjoibmV3dXNlcmZvcmV2ZXIiLCJhIjoiY2o2M3d1dTZiMGZobzMzbnp2Z2NiN3lmdyJ9.cQFKe3F3ovbfxTsM9E0ZSQ'

with open('neigh_id.geojson') as f:
    geojson = json.loads(f.read())

#neighs_data = pd.read_csv('neigh_data.csv', dtype={'id': object})



def content(date_received=None):

	if not date_received:
		airbnb_date = airbnb[airbnb['Fecha_Corte']=='2019-02-01']
	else:
		airbnb_date = airbnb[airbnb['Fecha_Corte']==date_received]

	return html.Div([
				dcc.Dropdown(
					id='periods-dropdown',
					options=[{'label':periods, 'value':periods} for periods in periods_data],
					value = periods_data[-1]
				),
				dcc.Graph(
					id = 'bogota-choropleth', 
					figure={ 
							'data': [go.Choroplethmapbox(
								geojson=geojson,
								locations=data_to_map['Cod_Barrio'],
								text=data_to_map['Barrio'],
								z=data_to_map['Media_Arriendo'],
								colorscale='Viridis',
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
			

def update_map(date_received=None):	

	

	start = time.time()
	
	if not date_received:
		airbnb_date = airbnb[airbnb['Fecha_Corte']=='2019-02-01']
	else:
		airbnb_date = airbnb[airbnb['Fecha_Corte']==date_received]
	end = time.time()
	print(end - start)
	
	start = time.time()
	airbnb_date.Media_Arriendo = airbnb_date.Media_Arriendo.astype(float)
	end = time.time()
	print(end - start)

	start = time.time()
	data_to_map = airbnb_date[['Cod_Barrio','Barrio','Media_Arriendo']]
	end = time.time()
	print(end - start)
	
	data_to_map.set_index('Cod_Barrio')
	
	#data_to_map = data_to_map[data_to_map['Media_Arriendo'] > 0]
		
	return { 
			'data': [go.Choroplethmapbox(
								geojson=geojson,
								locations=data_to_map['Cod_Barrio'],
								text=data_to_map['Barrio'],
								z=data_to_map['Media_Arriendo'],
								colorscale='Viridis',
								colorbar_title="Values"
							)],
							'layout': go.Layout(
									mapbox_style="light",
									mapbox_accesstoken=token,
									mapbox_zoom=9,
									mapbox_center = {"lat": 4.6918154, "lon": -74.0765448}
							)
					}
