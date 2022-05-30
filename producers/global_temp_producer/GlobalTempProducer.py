import os
import json
import argparse
import time

import pandas as pd
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable

from producers.BaseProducer import BaseProducer

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
CONTROL_TOPIC = os.environ.get("CONTROL_TOPIC")


class GlobalTempProducer(BaseProducer):

    def load_dataset(self):
        return self.load_global_temps()

    def load_global_temps(self):
        print("loading data...")
        # could be swapped to streaming from disk. Then, without using pandas
        df = pd.read_csv(f"{self.data_source.rstrip('/')}/graph.txt", delimiter="\s+", names=["year", "no_smoothing", "lowess_smoothing"], skiprows=5)
        df.columns = [c.lower() for c in df.columns]
        self.key = "year"
        return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data streaming utility for sending climate datasets to kafka")
    parser.add_argument("-d", "--input_dir", help="directory to where to find the data")

    args = parser.parse_args()

    producer = GlobalTempProducer(args.input_dir)
    producer.streaming_loop()
