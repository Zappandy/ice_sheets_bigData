import json
import argparse
import pandas as pd
import os
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")

def connect_to_kafka(server):
    producer = KafkaProducer(bootstrap_servers=server,
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                             key_serializer=lambda s: s.encode('utf-8'))
    return producer


def load_sea_ice_extent(data_dir):
    # could be swapped to streaming from disk. Then, without using pandas
    df_north = pd.read_csv(f"{data_dir.rstrip('/')}/N_seaice_extent_daily_v3.0.csv")
    df_north = df_north.drop(0)
    df_north["Hemisphere"] = "N"
    df_south = pd.read_csv(f"{data_dir.rstrip('/')}/S_seaice_extent_daily_v3.0.csv")
    df_south = df_south.drop(0)
    df_south["Hemisphere"] = "S"

    df_combined = pd.concat([df_north, df_south], axis=0).reset_index(drop=True)
    df_combined.columns = [c.strip() for c in df_combined.columns]

    for c in ['Year', 'Month', 'Day', 'Extent', 'Missing']:
        df_combined[c] = pd.to_numeric(df_combined[c])

    df_combined = df_combined.drop(["Source Data"], axis=1)

    return df_combined


def stream_df_to_kafka(producer, topic, key, df):
    for i, row in df.iterrows():
        producer.send(topic=topic, value=row.to_json(), key=row[key])

# example command
# send_data.py --dataset_name SeaIceExtent --input_dir ../../data/sea_ice_extent/ --topic SeaIceExtent --server localhost:9092
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data streaming utility for sending climate datasets to kafka")
    parser.add_argument("-ds", "--dataset_name", help="the name of the dataset to load")
    parser.add_argument("-d", "--input_dir", help="directory to where to find the data")
    # parser.add_argument("-t", "--topic", help="kafka topic to stream the data to")
    # parser.add_argument("-s", "--server", help="kafka server to stream the data to")
    parser.add_argument("-r", "--rate", help="rate at which the events are sent. Events per second")
    #TODO add arguments for sending fast, slow, k at a time, interactive, shuffled or ordered...

    args = parser.parse_args()

    key = None
    df_data = None
    topic = TOPIC_NAME
    server = KAFKA_BROKER_URL

    # change that to env variables as well
    if args.dataset_name == "SeaIceExtent":
        key = "Hemisphere"
        df_data = load_sea_ice_extent(args.input_dir)

    try:
        kafka_producer = connect_to_kafka(server)
    except NoBrokersAvailable as e:
        print(f"No brokers available on '{server}'")
        kafka_producer = None

    stream_df_to_kafka(producer=kafka_producer, topic=topic, key=key, df=df_data)
