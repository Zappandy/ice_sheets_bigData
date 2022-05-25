import os
import json
import argparse
import time

import pandas as pd
import multiprocessing
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
CONTROL_TOPIC = os.environ.get("CONTROL_TOPIC")


class IceSheetsProducer:
    def __init__(self, data_source):
        self.data_source = data_source
        self.data_df = self.load_sea_ice_extent()
        self.server = KAFKA_BROKER_URL
        self.topic = TOPIC_NAME
        self.kafka_producer = self.get_kafka_producer()
        self.kafka_control_listener = self.get_kafka_control_listener()

        self.remaining_ind = len(self.data_df)

        # column name for which column in DF to use as partition key
        self.key = "Hemisphere"

    def load_sea_ice_extent(self):
        print("loading data...")
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
        print("data loading complete")
        return df_combined

    def next(self):
        try:
            row = self.data_df.iloc[-self.remaining_ind]
            self.remaining_ind -= 1
            return json.loads(row.to_json())
        except IndexError:
            return None  # should be EndOfIteration or something like that

    def has_next(self):
        return self.remaining_ind > 0

    def get_kafka_producer(self):
        print("connecting to kafka broker")
        prod = KafkaProducer(bootstrap_servers=self.server,
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                             key_serializer=lambda s: s.encode('utf-8'))
        print("connected")
        return prod

    def get_kafka_control_listener(self):
        consumer = KafkaConsumer(CONTROL_TOPIC, group_id="control",
                                 bootstrap_servers=[self.server],
                                 # consumer_timeout_ms=LISTENER_TIMEOUT,
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        return consumer

    def streaming_loop(self):
        go = True
        pause = True
        speed = 0  # 0 is full speed, speed is determined by number of milliseconds of timeout per iteration

        print("ice sheet processor ready on standby")
        i = 0
        while go and self.has_next():
            # control structure
            # ideally this would set the speed and pause values asynchronously in another process for improved
            # performance
            control_record = self.kafka_control_listener.poll(1)
            control = control_record.values()
            if control:
                for c in control:
                    for c_vals in c:
                        control_vals = c_vals.value
                        if "topic" in control_vals and control_vals["topic"] == self.topic:
                            try:
                                pause = control_vals["pause"]
                                if pause:
                                    print("pausing...")
                                else:
                                    print("unpausing...")
                            except KeyError:
                                pass
                            try:
                                speed = control_vals["speed"]
                                if speed > 0:
                                    print(f"set speed to {speed}")
                            except KeyError:
                                pass
            if pause:
                continue

            if speed > 0:
                time.sleep(speed/1000)

            # data streaming
            elm = self.next()
            self.kafka_producer.send(topic=self.topic, value=elm, key=elm[self.key])
            i += 1

            if i % 1000 == 0:
                print(f"sent messages: {i}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data streaming utility for sending climate datasets to kafka")
    parser.add_argument("-d", "--input_dir", help="directory to where to find the data")

    args = parser.parse_args()

    producer = IceSheetsProducer(args.input_dir)
    producer.streaming_loop()
