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


class CaribouProducer(BaseProducer):

    def load_dataset(self):
        return self.load_caribou_population()

    def load_caribou_population(self):
        print("loading data...")
        # could be swapped to streaming from disk. Then, without using pandas
        df = pd.read_excel(f"{self.data_source.rstrip('/')}/03_Tab01_CaribouFInal.xlsx")
        self.key = "Year"
        return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data streaming utility for sending climate datasets to kafka")
    parser.add_argument("-d", "--input_dir", help="directory to where to find the data")

    args = parser.parse_args()

    producer = CaribouProducer(args.input_dir)
    producer.streaming_loop()
