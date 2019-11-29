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
            html.H2(children="Bogota", className='h2-title'),
        ],
        className='study-browser-banner row'
    ),
    dcc.Tabs(id="bogota-tabs", value='tabs-container', children=[
        dcc.Tab(label='Principal', value='main'), 
        dcc.Tab(label='Cálculo del índice', value='index-calculation'), 
		dcc.Tab(label='Revisión de barrios', value='neighborhood-review'), 
		dcc.Tab(label='Comparación', value='compare') 
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
		
		
if __name__ == "__main__":
    app.run_server(debug=True)
	