import os
import json
from kafka import KafkaConsumer
from cassandra.cluster import Cluster
import argparse


class CassandraSink:
    def __init__(self, broker_url, topic, cass_config):
        self.server = broker_url
        self.topic = topic

        self.cass_keyspace = cass_config["keyspace"]
        self.cass_url = cass_config["cass_url"]
        self.cass_table = cass_config["cass_table"]
        self.topic_keys, self.cass_cols = zip(*cass_config["keys_cols"].items())

        print("connecting to kafka...")
        self.consumer = self.get_kafka_consumer()
        print("connected")

        print("connecting to cassandra...")
        self.cassandra_session = self.get_cassandra_session()
        print("connected")

    def get_kafka_consumer(self):
        return KafkaConsumer(self.topic, group_id="debug",
                             bootstrap_servers=[self.server],
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    def get_cassandra_session(self):
        cluster = Cluster([self.cass_url])
        session = cluster.connect()
        session.set_keyspace(self.cass_keyspace)
        print("testing connection")
        try:
            session.execute(f'SELECT * FROM {self.cass_table}')
            print("connected")
            return session
        except Exception as e:
            print("failed to connect to cassandra")
            print(e)
            exit(1)

    def run_sink(self):
        data_mapping = ", ".join([f"%({k})s" for k in self.topic_keys])
        cols = ['"' + c + '"' for c in self.cass_cols]
        insert_statement = f"INSERT INTO  {self.cass_table} ({', '.join(cols)}) VALUES ({data_mapping})"
        print(data_mapping)
        print(insert_statement)
        for msg in self.consumer:
            vals = msg.value
            vals_ordered = {k:vals[k] for k in self.topic_keys}
            print(vals)
            self.cassandra_session.execute(insert_statement, vals_ordered)


if __name__ == "__main__":
    """
    parser = argparse.ArgumentParser(desc="create a kafka sink for cassandra (the sketchy way)")
    parser.add_argument("-b", "--broker-url", help="kafka url")
    parser.add_argument("-t", "--topic", help="kafka topic to read from")
    parser.add_argument("-c", "--cass_conf", help="cassandra config json file")
    args = parser.parse_args()
    """
    c = os.environ.get("CASS_CONF")
    b = os.environ.get("KAFKA_BROKER_URL")
    t = os.environ.get("LISTEN_TO_TOPICS")

    with open(c, "r") as in_f:
        c_conf = json.load(in_f)

    sink = CassandraSink(broker_url=b, topic=t, cass_config=c_conf)
    sink.run_sink()
