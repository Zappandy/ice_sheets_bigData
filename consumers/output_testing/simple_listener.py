import os
import json
from kafka import KafkaConsumer

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
LISTEN_TO_TOPICS = os.environ.get("LISTEN_TO_TOPICS")
LISTENER_TIMEOUT = int(os.environ.get("LISTENER_TIMEOUT"))


if __name__ == "__main__":
    print("Trying to connect")
    print("listening to topic:", LISTEN_TO_TOPICS)
    consumer = KafkaConsumer(LISTEN_TO_TOPICS, group_id="debug",
                             bootstrap_servers=[KAFKA_BROKER_URL],
                             consumer_timeout_ms=LISTENER_TIMEOUT,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    print(F"Connected, consuming messages (will wait for {LISTENER_TIMEOUT/1000} seconds)")

    # TODO wait until process is killed
    for msg in consumer:
        print(f"{msg.topic}, {msg.partition}, {msg.offset}, {msg.key}, {msg.value}")