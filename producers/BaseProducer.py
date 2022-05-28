import json
import os
import time

from kafka import KafkaProducer, KafkaConsumer


class BaseProducer:
    def __init__(self, data_source):
        # column name for which column in DF to use as partition key
        self.key = None
        self.data_source = data_source
        self.data_df = self.load_dataset()
        self.server = os.environ.get("KAFKA_BROKER_URL")
        self.topic = os.environ.get("TOPIC_NAME")
        self.control_topic = os.environ.get("CONTROL_TOPIC")
        self.kafka_producer = self.get_kafka_producer()
        self.kafka_control_listener = self.get_kafka_control_listener()

        self.remaining_ind = len(self.data_df)

        print(self.data_df.columns)

    def load_dataset(self):
        pass

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
        print("connecting to kafka broker for producing")
        prod = KafkaProducer(bootstrap_servers=self.server,
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                             key_serializer=lambda s: s.encode('utf-8'))
        print("connected")
        return prod

    def get_kafka_control_listener(self):
        print(f"connecting on topic {self.control_topic} for consuming")
        consumer = KafkaConsumer(self.control_topic,
                                 bootstrap_servers=[self.server],
                                 # consumer_timeout_ms=LISTENER_TIMEOUT,
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        print("connected")
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
            print(self.key)
            print(elm)
            self.kafka_producer.send(topic=self.topic, value=elm, key=elm[self.key])
            i += 1

            if i % 1000 == 0:
                print(f"sent messages: {i}")