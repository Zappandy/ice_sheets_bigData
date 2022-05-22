import os
import json
import pandas as pd
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")


class IceSheetsProducer:
    def __init__(self, data_source):
        self.data_source = data_source
        self.data_df = self.load_sea_ice_extent()
        self.kafka_producer = self.get_kafka_producer()

        self.remaining_ind = len(self.data_df)

        self.server = KAFKA_BROKER_URL
        self.topic = TOPIC_NAME
        # column name for which column in DF to use as partition key
        self.key = "Hemisphere"

    def load_sea_ice_extent(self):
        # could be swapped to streaming from disk. Then, without using pandas
        df_north = pd.read_csv(f"{self.data_source.rstrip('/')}/N_seaice_extent_daily_v3.0.csv")
        df_north = df_north.drop(0)
        df_north["Hemisphere"] = "N"
        df_south = pd.read_csv(f"{self.data_source.rstrip('/')}/S_seaice_extent_daily_v3.0.csv")
        df_south = df_south.drop(0)
        df_south["Hemisphere"] = "S"

        df_combined = pd.concat([df_north, df_south], axis=0).reset_index(drop=True)
        df_combined.columns = [c.strip() for c in df_combined.columns]

        for c in ['Year', 'Month', 'Day', 'Extent', 'Missing']:
            df_combined[c] = pd.to_numeric(df_combined[c])

        df_combined = df_combined.drop(["Source Data"], axis=1)
        df_combined = df_combined.sort_values(['Year', 'Month', 'Day'])

        return df_combined

    def next(self):
        try:
            row = self.data_df.iloc[-self.remaining_ind]
            self.remaining_ind -= 1
            return row.to_json()
        except IndexError:
            return None  # should be EndOfIteration or something like that

    def has_next(self):
        return self.remaining_ind > 0

    def get_kafka_producer(self):
        producer = KafkaProducer(bootstrap_servers=self.server,
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                                 key_serializer=lambda s: s.encode('utf-8'))
        return producer

    def streaming_loop(self):
        go = True
        while go and self.has_next():
            elm = self.next()
            self.send(topic=self.topic, value=elm.to_json(), key=elm[self.key])
            # TODO: add control listener here. Listen to kafka control topic


if __name__ == "__main__":

