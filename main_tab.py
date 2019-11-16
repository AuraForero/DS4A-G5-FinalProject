import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import json
import pandas as pd

token = 'pk.eyJ1IjoibmV3dXNlcmZvcmV2ZXIiLCJhIjoiY2o2M3d1dTZiMGZobzMzbnp2Z2NiN3lmdyJ9.cQFKe3F3ovbfxTsM9E0ZSQ'

with open('neigh_id.geojson') as f:
    geojson = json.loads(f.read())

neighs_data = pd.read_csv('neigh_data.csv', dtype={'id': object})

def content():
	return  html.Div([
				dcc.Graph(
					id = 'bogota-choropleth', 
					figure={ 
							'data': [go.Choroplethmapbox(
								geojson=geojson,
								locations=neighs_data['id'],
								text=neighs_data['neighborhood'],
								z=neighs_data['value'],
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