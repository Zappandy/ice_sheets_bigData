from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from flask import Flask
import pandas as pd
from cassandra.cluster import Cluster
import dash
from contextlib import closing
import socket


def find_open_ports():
    for port in range(1, 8081):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            res = sock.connect_ex(('localhost', port))
            if res == 0:
                yield port

available_ports = list(find_open_ports())
print(available_ports)

#getting conection with cassandra
# cluster = Cluster(['0.0.0.0'],port=9042)
# session = cluster.connect()
# keyspace = "icesheet_keyspace"

# server = Flask(__name__)
# app = dash.Dash(server=server, external_stylesheets=[dbc.themes.FLATLY])
# app.title = 'Dashboard'
  
# session.set_keyspace(keyspace)
# # session.execute('SELECT * FROM icesheetreport')
# rows = session.execute('SELECT hemisphere, day, extend, missing FROM icesheetreport')
# for r in rows:
#     print(r.day, r.extend, r.missing)

  
# app.layout = dbc.Container([ 
  
#     dbc.Row(dbc.Col(html.H2("Your Amazing Dashboard"), width={'size': 12, 'offset': 0, 'order': 0}), style = {'textAlign': 'center', 'paddingBottom': '1%'}),
  
#     dbc.Row(dbc.Col(dcc.Loading(children=[dcc.Graph(id ='your-graph'),
#                                         dcc.Slider(id='year-slider',
#                                                     min=df['year'].min(),
#                                                     max=df['year'].max(),
#                                                     value=df['year'].min(),
#                                                     marks={str(year): str(year) for year in df['year'].unique()},
#                                                     step=None)
#                                         ], color = '#000000', type = 'dot', fullscreen=True ) ))])
  
# @app.callback(
#     Output('your-graph', 'figure'),
#     Input('year-slider', 'value'))
# def update_figure(selected_year):
#     filtered_df = df[df.year == selected_year]
  
#     fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
#                     size="pop", color="continent", hover_name="country",
#                     log_x=True, size_max=55)
  
#     fig.update_layout(transition_duration=500)
  
#     return fig
  
# if __name__=='__main__':
#      app.run_server()