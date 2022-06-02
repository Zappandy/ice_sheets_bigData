#import datetime
#
##from dash.dependencies import Output, Input, State
##from kafka import KafkaConsumer
#import dash_bootstrap_components as dbc
#import dash_core_components as dcc
#import dash_html_components as html
#import plotly.express as px
#from flask import Flask
#import os, os.path, sys
##import json
##import pandas as pd
##from cassandra.cluster import Cluster
#import dash
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots
#
#
#sys.path.append(os.path.abspath('../'))
## getting conection with cassandra
## cluster = Cluster()
## session = cluster.connect('cassandra-1')
#
##keyspace = "icesheet_keyspace"
##cluster = Cluster(['cassandra-1'])
##session =  cluster.connect()
#
#server = Flask(__name__)
#app = dash.Dash(server=server, external_stylesheets=[dbc.themes.FLATLY])
#app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
#app.title = 'Icesheets_Dashboard'
#
##session.set_keyspace(keyspace)
##session.execute('SELECT * FROM icesheetreport')
#
## stream connections for predictions and visualizations
#
#KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
#LISTEN_TO_TOPICS = os.environ.get("LISTEN_TO_TOPICS")
#LISTENER_TIMEOUT = int(os.environ.get("LISTENER_TIMEOUT"))
#
##TOPIC_NAME = os.environ.get("TOPIC_NAME")
#
#X_ice_extent = list()
#Y_ice_extent = list()
#  
#consumer = KafkaConsumer(LISTEN_TO_TOPICS, group_id="raw_streams",
#                         bootstrap_servers=[KAFKA_BROKER_URL],
#                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))  # ocean and caribou?? where at
#
#def num_records(consum, n=1000):
#    try:
#        records = consum.poll(1000 * 5)
#        elms = list(records.values())
#    except Exception as e:
#        print("error polling records")
#        print(e)
#        elms = list()
#    try:
#        multiple_streams = [stream.value for stream in elms]
#    except IndexError as e:
#        print("communicating with streams...")
#    return multiple_streams
#
## define a key
## icesheet_df = pd.DataFrame.from_records(num_records(consumer))
#
## heatmap = px.imshow([extension])
##print(icesheet_df.head(10))
#
#"""if icesheet_df.empty:
#    print("can't enter yet...")
#
#    icesheet_df = pd.DataFrame.from_dict({"Hemisphere": ['N', 'S'], "Year": [0, 0],
#                                          "Month": [0, 0], "Day": [0, 0],
#                                          "Extent": [0.0, 0.0], "Missing": [0.0, 0.0]})
#"""
#
#
#app.layout = dbc.Container([
#
#    dbc.Row(dbc.Col(html.H2("Icesheet Dashboard"), width={'size': 12, 'offset': 0, 'order': 0}), style={'textAlign': 'center', 'paddingBottom': '1%'}),
#    dbc.Row(dbc.Col(dcc.Loading(
#        children=[dcc.Graph(id='north_extension', animate=True),
#                  dcc.Interval(
#                            id='interval-component',
#                            interval=1*5000, # in milliseconds
#                            n_intervals=0
#                        )
#                  ],
#        style={'width': '49%', 'display': 'inline-block'})))
#])
#
#"""
#dbc.Row(dbc.Col(dcc.Loading(
#    children=[dcc.Graph(id='north_preds', animate=True),
#              dcc.Interval(
#                        id='interval-component2',
#                        interval=1*5000, # in milliseconds
#                        n_intervals=0
#                    )
#              ],
#"""
#
## Multiple components can update everytime interval gets fired.
#@app.callback(Output('north_extension', 'figure'),
#              Input('interval-component', 'n_intervals'))
#def update_graph_live(n):
#    # kafka consumer goes here
#    new_data = num_records(consumer)
#    print(len(new_data))
#    X_ice_extent.extend([datetime.date(d["Year"], d["Month"], d["Day"]) for d in new_data if d["Hemisphere"] == "N"])
#    Y_ice_extent.extend([d["Extent"] for d in new_data if d["Hemisphere"] == "N"])
#
#    trace1 = go.Scatter(
#        x=list(X_ice_extent),
#        y=list(Y_ice_extent),
#        name='Scatter',
#        mode='lines+markers'
#    )
#
#    return [{'data': [trace1], 'layout': go.Layout(xaxis=dict(range=[min(X_ice_extent), max(X_ice_extent)]),
#                                                yaxis=dict(range=[min(Y_ice_extent), max(Y_ice_extent)]))}]
#
#"""
#@app.callback(Output('north_preds', 'figure'),
#              Input('interval-component2', 'n_intervals'))
#def update_preds_live():
#    new_data_pre = num_records(consumer2)
#    print(len(new_data_pre))
#    X_ice_pred, Y_ice_pred = zip(*[(datetime.date(p["Year"], p["Month"], p["Day"]), p["pred"]) for p in new_data_pre[-1].value["predictions"]])
#    trace2 = go.Scatter(
#        x=list(X_ice_pred),
#        y=list(Y_ice_pred),
#        name='Prediction',
#        mode='lines+markers'
#    )
#    return [{'data': [trace2], 'layout': go.Layout(xaxis=dict(range=[min(X_ice_pred), max(X_ice_pred)]),
#                                                yaxis=dict(range=[min(Y_ice_pred), max(Y_ice_pred)]))}]
#"""
#
#if __name__=='__main__':
#     #app.run_server(port=5000, debug=True)
#     #app.run_server(host='0.0.0.0', port=5000, debug=True)
#     app.run(host='0.0.0.0', port=80, debug=True)
