import logging
import time
import subprocess

log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

KEYSPACE = "icesheet_keyspace"

class cassandraKeyspace:

    def __init__(self):
        pass  # call method to connecto to cluster in cassandra

def createKeySpace():
    time.sleep(5)
    contact_points= [f'172.21.0.{i}' for i in range(1, 10)]
    cluster = Cluster(contact_points=contact_points,port=9042)  
    #cluster = Cluster(contact_points=['172.21.0.5'],port=9042)  
    #cluster = Cluster(contact_points=["localhost"],port=9042)  # 172.21.0.1, order of containers
    session = cluster.connect()

    log.info("tito... help")
    raise SystemExit

    log.info("Creating keyspace...")

    try:
        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS %s
            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' };
            """ % KEYSPACE)

        log.info("setting keyspace...")
        session.set_keyspace(KEYSPACE)

        log.info("creating table...")
        session.execute("""
            CREATE TABLE mytable (
                _year INT,
                _month INT,
                _day INT,
                extend FLOAT,
                missing FLOAT,
                hemisphere TEXT,
                PRIMARY KEY (hemisphere, extend)
            );
            """)
    except Exception as e:
        log.error("Unable to create keyspace")
        log.error(e)
def dropKeySpace():  # dropping key_space if needs to be deleted
    """
    DROP KEYSPACE IF EXISTS "icesheet_keyspace";
    """
    pass

createKeySpace()

# https://docs.datastax.com/en/developer/python-driver/3.24/api/cassandra/cluster/
# https://medium.com/nerd-for-tech/cassandra-multinode-setup-on-a-single-host-using-docker-fe3d8b844f52
# https://medium.com/rahasak/end-to-end-streaming-from-kafka-to-cassandra-447d0e6ba25a
# https://stackoverflow.com/questions/17157721/how-to-get-a-docker-containers-ip-address-from-the-host
# https://devtonight.com/questions/how-to-assign-static-ip-addresses-to-docker-compose-containers
# https://runnable.com/docker/basic-docker-networking
# https://runnable.com/docker/docker-compose-networking
# https://www.linkedin.com/pulse/creating-cassandra-keyspace-table-docker-start-up-amon-peter
# https://digitalis.io/blog/apache-cassandra/getting-started-with-kafka-cassandra-connector/
# https://github.com/digitalis-io/kafka-connect-cassandra-blog

# https://blog.digitalis.io/containerized-cassandra-cluster-for-local-testing-60d24d70dcc4
# https://github.com/OneCricketeer/apache-kafka-connect-docker
