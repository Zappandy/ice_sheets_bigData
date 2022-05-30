from dash.dependencies import Output, Input, State
from kafka import KafkaConsumer
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import os
import json
from flask import Flask
import pandas as pd
from cassandra.cluster import Cluster
import dash

# getting conection with cassandra
# cluster = Cluster()
# session = cluster.connect('cassandra-1')

#keyspace = "icesheet_keyspace"
#cluster = Cluster(['cassandra-1'])
#session =  cluster.connect()

server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.FLATLY])
app.title = 'Icesheets_Dashboard'
  
#session.set_keyspace(keyspace)
#session.execute('SELECT * FROM icesheetreport')

# print(session.execute('SELECT * FROM icesheetreport'))
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
# stream connections for predictions and visualizations

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
LISTEN_TO_TOPICS = os.environ.get("LISTEN_TO_TOPICS")
LISTENER_TIMEOUT = int(os.environ.get("LISTENER_TIMEOUT"))
print(f"kafka_broker_url: {KAFKA_BROKER_URL}")
print(f"listen_to_topics: {LISTEN_TO_TOPICS}")
print(f"listener_timeout: {LISTENER_TIMEOUT}")

#LISTENER_TIMEOUT = 1000
#TOPIC_NAME = os.environ.get("TOPIC_NAME")
#
#  
#consumer = KafkaConsumer(LISTEN_TO_TOPICS, group_id="raw_streams",
#                         bootstrap_servers=[KAFKA_BROKER_URL],
#                         consumer_timeout_ms=LISTENER_TIMEOUT,
#                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))
#
#
#for msg in consumer:
#    print(f"{msg.topic}, {msg.partition}, {msg.offset}, {msg.key}, {msg.value}")
#
#print("ended with titoes")
#app.layout = dbc.Container([ 
#  
#    dbc.Row(dbc.Col(html.H2("Your Amazing Dashboard"), width={'size': 12, 'offset': 0, 'order': 0}), style = {'textAlign': 'center', 'paddingBottom': '1%'}),
#  
#    dbc.Row(dbc.Col(dcc.Loading(children=[dcc.Graph(id ='your-graph'),
#                                        dcc.Slider(id='year-slider',
#                                                    min=df['year'].min(),
#                                                    max=df['year'].max(),
#                                                    value=df['year'].min(),
#                                                    marks={str(year): str(year) for year in df['year'].unique()},
#                                                    step=None)
#                                        ], color = '#000000', type = 'dot', fullscreen=True ) ))])
#  
#@app.callback(
#    Output('your-graph', 'figure'),
#    Input('year-slider', 'value'))
#def update_figure(selected_year):
#    filtered_df = df[df.year == selected_year]
#  
#    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
#                    size="pop", color="continent", hover_name="country",
#                    log_x=True, size_max=55)
#  
#    fig.update_layout(transition_duration=500)
#  
#    return fig
#  
#if __name__=='__main__':
#     app.run_server()
