from kafka import KafkaConsumer, KafkaProducer
import os
import json
import numpy as np

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
LISTEN_TO_TOPICS = os.environ.get("LISTEN_TO_TOPICS")
LISTENER_TIMEOUT = int(os.environ.get("LISTENER_TIMEOUT"))
TOPIC_NAME = os.environ.get("TOPIC_NAME")
POLY_DEGREE = os.environ.get("POLY_DEGREE")


class IceSheetsPredictor:
    def __init__(self):
        self.server = KAFKA_BROKER_URL
        self.listen_to_topics = LISTEN_TO_TOPICS
        self.listener_timeout = LISTENER_TIMEOUT
        self.topic = TOPIC_NAME
        self.key = "Hemisphere"
        self.consumer = self.get_kafka_consumer()
        self.producer = self.get_kafka_producer()
        self.max_prediction_year = 2025
        self.poly_degree = POLY_DEGREE
        # self.model = self.create_model()
        print("init done")

    def get_kafka_consumer(self):
        print("connecting consumer to kafka broker")
        cons = KafkaConsumer(self.listen_to_topics,
                             bootstrap_servers=[self.server],
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

    def create_model(self):
        import numpy as np
        model = Pipeline([('poly', PolynomialFeatures(degree=int(self.poly_degree))),
                          ('linear', LinearRegression(fit_intercept=False))])
        return model

    def processing_loop(self):
        print("processing messages...")
        go = True

        data = dict()
        data["N"] = list()
        data["S"] = list()
        start_date = dict()
        start_date["N"] = None
        start_date["S"] = None

        year_months_past = dict()
        year_months_past["N"] = list()
        year_months_past["S"] = list()
        year_months_future = dict()
        year_months_future["N"] = list()
        year_months_future["S"] = list()

        ret = dict()
        ret["N"] = list()
        ret["S"] = list()

        offset_wait = 20
        while go:
            try:
                records = self.consumer.poll(1000*5)
                elms = list(records.values())[0]
            except Exception as e:
                print("error polling records")
                print(e)
                continue
            for cur_rec in elms:
                elm = cur_rec.value

                if elm["Day"] == 1:
                    hem = elm["Hemisphere"]

                    if start_date[hem] is None:
                        start_date[hem] = (elm["Year"], elm["Month"], elm["Day"])
                        year_months_past[hem].append(0)
                        year_months_future[hem] = list(range(((self.max_prediction_year - elm["Year"]) * 12) - offset_wait))
                        ret[hem] = [{"year": elm["Year"], "month": j, "day": 1} for j in range(elm["Month"], 13)]
                        ret[hem].extend([{"year": i, "month": j, "day": 1} for i in range(elm["Year"]+1,
                                                                                          self.max_prediction_year)
                                         for j in range(1, 13)])
                        ret[hem] = ret[hem][offset_wait:]
                    data[hem].append(elm["Extent"])
                    if len(data[hem]) > 1:
                        year_months_past[hem].append(year_months_past[hem][-1]+1)

                    year_months_future[hem] = year_months_future[hem][1:]
                    ret[hem] = ret[hem][1:]

                    print(data[hem])
                    print(year_months_past[hem])
                    print(year_months_future[hem])
                    if len(data[hem]) > offset_wait:
                        model = self.create_model()
                        model.fit(np.asarray(year_months_past[hem]).reshape(-1, 1), data[hem])
                        pred = model.predict(np.asarray(year_months_future[hem]).reshape(-1, 1))
                        pred_vals = [{**e, **{"pred": p}} for e, p in zip(ret[hem], pred)]
                        ret_dict = {
                            "year": elm["Year"],
                            "month": elm["Month"],
                            "day": elm["Day"],
                            "Hemisphere": hem,
                            "extent": elm["Extent"],
                            "predictions": pred_vals
                        }
                        print("sending...")
                        self.producer.send(topic=self.topic, value=ret_dict, key=ret_dict[self.key])


if __name__ == "__main__":
    processor = IceSheetsPredictor()
    processor.processing_loop()

