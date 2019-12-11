import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import random
from dash.dependencies import Input, Output, State
import json
from urllib.request import urlopen
import main_tab
import index_calculation
import neighborhood_review
import compare

app = dash.Dash(
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
	html.Div(
		children=[
			html.Div(
				children = [html.Div( className='custom-header',
					children = [
					html.Div(
						html.Img(src=app.get_asset_url('bogota.png'))		
					),
					html.Div(
						html.H2(children="Coolness Index", className='h2-title')
					)
					]
				)]
			)
		]
    ),
    dcc.Tabs(id="bogota-tabs", value='tabs-container', children=[
        dcc.Tab(label='Cálculo del índice', value='index-calculation', className='my-tabs'),
		dcc.Tab(label='Comparación', value='compare', className='my-tabs'),
		dcc.Tab(label='Revisión de barrios', value='neighborhood-review', className='my-tabs'),
		dcc.Tab(label='Descripción de variables', value='main', className='my-tabs'),
	]),
	html.Div(id='tabs-content')	
])

@app.callback(Output('tabs-content', 'children'),
              [Input('bogota-tabs', 'value')])
def render_content(tab):
	if tab == 'main':
		return main_tab.content();
	elif tab == 'index-calculation':
		return index_calculation.content()
	elif tab == 'neighborhood-review':
		return neighborhood_review.content()		
	elif tab == 'compare':
		return compare.content()

@app.callback(
    dash.dependencies.Output('bogota-choropleth', 'figure'),
    [dash.dependencies.Input('periods-dropdown', 'value')])
def main_update_output(value):
	print('callable')
	#return 'You have selected "{}"'.format(value)	
	return main_tab.update_map(value)
	
@app.callback(
	dash.dependencies.Output('index-map-content', 'children'),
	[dash.dependencies.Input('show-index-check', 'value')]
)
def index_show_map(checklist_values):
	if len(checklist_values) == 0:
		return html.H2(children="", className='h2-title')
	else:
		return index_calculation.update_index_map()
	
@app.callback(
	dash.dependencies.Output('graph-boxplot-index', 'figure'),
	[dash.dependencies.Input('show-index-sd', 'value')]
)
def index_show_map(checklist_values):
	if len(checklist_values) == 0:
		return index_calculation.update_boxplot_index_no_sd()
	else:
		return index_calculation.update_boxplot_index_sd()

@app.callback(
	dash.dependencies.Output('elbow-content', 'children'),
	[dash.dependencies.Input('show-elbow', 'value')]
)
def elbow_show_graph(checklist_values):
	if len(checklist_values) == 0:
		return html.H2(children="")
	else:
		return index_calculation.update_elbow()

@app.callback(
    dash.dependencies.Output('comparing-scatterpolar', 'figure'),
    [dash.dependencies.Input('barrios-dropdown-1', 'value'), 
	 dash.dependencies.Input('barrios-dropdown-2', 'value')])
def compare_update_radar(barrio1, barrio2):
	return compare.update_radar_chart(barrio1, barrio2)
	
		
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050, debug=True)
	