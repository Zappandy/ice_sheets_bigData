from dash.dependencies import Output, Input, State
from kafka import KafkaConsumer
#from chart_studio.plotly import plot, iplot  for online/cloud plots
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import os, os.path, sys
import json
from flask import Flask
import pandas as pd
from cassandra.cluster import Cluster
import dash
import plotly.graph_objects as go

sys.path.append(os.path.abspath('../'))
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

#TOPIC_NAME = os.environ.get("TOPIC_NAME")

  
consumer = KafkaConsumer(LISTEN_TO_TOPICS, group_id="raw_streams",
                         bootstrap_servers=[KAFKA_BROKER_URL],
                         consumer_timeout_ms=LISTENER_TIMEOUT,
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

def num_records(consum, n=1000):
    for i, msg in enumerate(consum):
        print(f"{msg.topic}, {msg.partition}, {msg.offset}, {msg.key}, {msg.value}")
        print(f"{type(msg.topic)}, {type(msg).partition}, {type(msg).offset}, {type(msg).key}, {type(msg).value}")
        if i == 30:
            break
        # records = consum.poll(n*5)
    # return list(records.values())[0]

# define a key
elms = num_records(consumer)
#icesheet_df = pd.DataFrame.from_records([el.value for el in elms])
#mask_df = icesheet_df["Hemisphere"] == 'N'
#north_df = icesheet_df[mask_df]
#south_df = icesheet_df[~mask_df]

#for i, msg in enumerate(consumer):
#    print(f"{msg.topic}, {msg.partition}, {msg.offset}, {msg.key}, {msg.value}")  # year, month, day, extend, missing, hemisphere
# extension = north_df["Extent"].tolist()
# years = north_df["Year"].tolist()
# months = north_df["Month"].tolist()

# heatmap = px.imshow([extension]) 
#print(icesheet_df.head(10))

fig_heatmap = go.Figure(data=go.Heatmap(
          x=[i for i in range(1, 30)],
          y=[i for i in range(1, 12)],
          z=[5, 14, 8],
          type = 'heatmap',
          colorscale = 'Viridis'))

app.layout = dbc.Container([
  
    dbc.Row(dbc.Col(html.H2("Icesheet Dashboard"), width={'size': 12, 'offset': 0, 'order': 0}), style={'textAlign': 'center', 'paddingBottom': '1%'}),
  
    # dbc.Row(dbc.Col(dcc.Loading(children=[dcc.Graph(id ='your-graph'),
    #                                     dcc.Slider(id='year-slider',
    #                                                 min=df['year'].min(),
    #                                                 max=df['year'].max(),
    #                                                 value=df['year'].min(),
    #                                                 marks={str(year): str(year) for year in df['year'].unique()},
    #                                                 step=None)
    #                                     ], color = '#000000', type = 'dot', fullscreen=True ) )),
dbc.Row(dbc.Col(dcc.Loading(
    children=[dcc.Graph(id='north_extension', figure=fig_heatmap)], style={'width': '49%', 'display': 'inline-block' })))
])
  
@app.callback(
    Output('your-graph', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
  
    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                    size="pop", color="continent", hover_name="country",
                    log_x=True, size_max=55)
  
    fig.update_layout(transition_duration=500)
  
    return fig

  
if __name__=='__main__':
     app.run_server()
     #app.run_server(host='0.0.0.0:80', port=5000, debug=True)
