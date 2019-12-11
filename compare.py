import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import json
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://elalbeiro:9988776655@extendedcase4.csuiz4fdxyvv.us-east-2.rds.amazonaws.com/postgres')




def plot_individual_radar(df, cols_radar, nbh_column, nbh_name):
	r = df[df[nbh_column]==nbh_name][cols_radar].values[0]
	theta = cols_radar
	viz_df = pd.DataFrame(dict(r=r,theta=theta))
	return viz_df


def content():
	
	query = '''
		SELECT DISTINCT
			cod_barrio 
			, cod_name
			, id as id_barrio
			, hurtos_norm as "Index Seguridad Robos"
			, accidentes_norm as "Index Seguridad Transporte"
			, alojamiento_norm as "Index Alojamientos"
			, sitp_norm as "Index Transporte Público"
			, restaurantes_norm as "Index Restaurantes y Bares"
			, parques_norm as "Index Parques Urbanos"
			, sitios_norm as "Index Sitios de Interés"
		FROM info_barrios_codigos
			'''

	df_index = pd.read_sql(query,engine.connect())
	
	cols_radar = list(['Index Seguridad Robos'
                   ,'Index Seguridad Transporte'
                   ,'Index Alojamientos'
                   ,'Index Transporte Público'
                   ,'Index Restaurantes y Bares'
                   ,'Index Parques Urbanos'
                   ,'Index Sitios de Interés'])
				   
	nbh_column='cod_name'
	
	nbh_name = '009222 ALTOS DE CHOZICA'
				   
	viz_df = plot_individual_radar(df=df_index, cols_radar=cols_radar, nbh_column=nbh_column, nbh_name=nbh_name)
	
	nbh_name_2 = '005632 BOCHICA'
	
	viz_df_2 = plot_individual_radar(df=df_index, cols_radar=cols_radar, nbh_column='cod_name',nbh_name=nbh_name_2)
	
	#Fill data of barrios
	barrios = pd.read_sql('select cod_barrio, barrio from barrios',engine.connect())
	barrios['cod_nombre_barrio'] = barrios['cod_barrio'] + ' ' + barrios['barrio']
	barrios_data = list(barrios['cod_nombre_barrio'])

	
	return html.Div([
			html.Div(
				className="row",
				children=[
					html.H5("Comparar barrios", className='my-subtitles' )
				]	
			),
			html.Div(
				className="row",
				children=[
					html.H6("Seleccionar barrio 1", className='my-subtitles' ), 
					dcc.Dropdown(
							id='barrios-dropdown-1',
							options=[{'label':barrio, 'value':barrio} for barrio in barrios_data], 
							value='009222 ALTOS DE CHOZICA'
					)
				]	
			),
			html.Div(
				className="row",
				children=[
					html.H6("Seleccionar barrio 2", className='my-subtitles' ), 
					dcc.Dropdown(
							id='barrios-dropdown-2',
							options=[{'label':barrio, 'value':barrio} for barrio in barrios_data], 
							value='005632 BOCHICA'
					)
				]	
			),
			dcc.Graph(
                    id='comparing-scatterpolar',
                    figure={
                        'data': [
							go.Scatterpolar(
							  r=viz_df.r,
							  theta=viz_df.theta,
							  fill='toself',
							  name=nbh_name
							), 
							go.Scatterpolar(
							  r=viz_df_2.r,
							  theta=viz_df_2.theta,
							  fill='toself',
							  name=nbh_name_2
							)
                        ]
                    }
            )
        ])
		

def update_radar_chart(barrio1, barrio2):
	print(barrio1)
	print(barrio2)
	
	query = '''
		SELECT DISTINCT
			cod_barrio 
			, cod_name
			, id as id_barrio
			, hurtos_norm as "Index Seguridad Robos"
			, accidentes_norm as "Index Seguridad Transporte"
			, alojamiento_norm as "Index Alojamientos"
			, sitp_norm as "Index Transporte Público"
			, restaurantes_norm as "Index Restaurantes y Bares"
			, parques_norm as "Index Parques Urbanos"
			, sitios_norm as "Index Sitios de Interés"
		FROM info_barrios_codigos
			'''

	df_index = pd.read_sql(query,engine.connect())
	
	cols_radar = list(['Index Seguridad Robos'
                   ,'Index Seguridad Transporte'
                   ,'Index Alojamientos'
                   ,'Index Transporte Público'
                   ,'Index Restaurantes y Bares'
                   ,'Index Parques Urbanos'
                   ,'Index Sitios de Interés'])
				   
	nbh_column='cod_name'
	
	nbh_name = barrio1
				   
	viz_df = plot_individual_radar(df=df_index, cols_radar=cols_radar, nbh_column=nbh_column, nbh_name=nbh_name)
	
	nbh_name_2 = barrio2
	
	viz_df_2 = plot_individual_radar(df=df_index, cols_radar=cols_radar, nbh_column='cod_name',nbh_name=nbh_name_2)
	
	#Fill data of barrios
	barrios = pd.read_sql('select cod_barrio, barrio from barrios',engine.connect())
	barrios['cod_nombre_barrio'] = barrios['cod_barrio'] + ' ' + barrios['barrio']
	barrios_data = list(barrios['cod_nombre_barrio'])
	
	return {
                        'data': [
							go.Scatterpolar(
							  r=viz_df.r,
							  theta=viz_df.theta,
							  fill='toself',
							  name=nbh_name
							), 
							go.Scatterpolar(
							  r=viz_df_2.r,
							  theta=viz_df_2.theta,
							  fill='toself',
							  name=nbh_name_2
							)
                        ]
                    }