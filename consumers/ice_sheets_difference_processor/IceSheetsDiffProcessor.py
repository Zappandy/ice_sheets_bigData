from kafka import KafkaConsumer, KafkaProducer
import os
import json

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
LISTEN_TO_TOPICS = os.environ.get("LISTEN_TO_TOPICS")
LISTENER_TIMEOUT = int(os.environ.get("LISTENER_TIMEOUT"))
TOPIC_NAME = os.environ.get("ICE_SHEET_DIFF_TOPIC")


class IceSheetsDiffProcessor:
    def __init__(self):
        self.server = KAFKA_BROKER_URL
        self.listen_to_topics = LISTEN_TO_TOPICS
        self.listener_timeout = LISTENER_TIMEOUT
        self.topic = TOPIC_NAME
        self.key = "Hemisphere"
        self.consumer = self.get_kafka_consumer()
        self.producer = self.get_kafka_producer()
        print("init done")

    def get_kafka_consumer(self):
        print("connecting consumer to kafka broker")
        cons = KafkaConsumer(self.listen_to_topics, group_id="debug",
                             bootstrap_servers=[KAFKA_BROKER_URL],
                             consumer_timeout_ms=LISTENER_TIMEOUT,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        print("consumer connected")
        return cons

    def get_kafka_producer(self):
        print("connecting producer to kafka broker")
        prod = KafkaProducer(bootstrap_servers=self.server,
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                             key_serializer=lambda s: s.encode('utf-8'))
        print("producer connected")
        return prod

    def processing_loop(self):
        print("processing messages...")
        go = True

        prev_s = 0
        prev_n = 0
        while go:
            # does not take into account the correct partitioning of the keys
            # this is currently a non-distributable version of the code
            try:
                records = self.consumer.poll(1000*5)
            except Exception as e:
                print("error polling records")
                print(e)
                continue
            elms = list(records.values())[0]
            print(len(elms))
            for cur_rec in elms:
                cur_elm = cur_rec.value
                cur_val = cur_elm["Extent"]
                if cur_elm[self.key] == "S":
                    diff = cur_val - prev_s
                elif cur_elm[self.key] == "N":
                    diff = cur_val - prev_n
                else:
                    diff = None

                cur_elm["Difference"] = diff
                print("sending...")
                self.producer.send(topic=self.topic, value=cur_elm, key=cur_elm[self.key])
                print(cur_elm)


if __name__ == "__main__":
    processor = IceSheetsDiffProcessor()
    processor.processing_loop()

