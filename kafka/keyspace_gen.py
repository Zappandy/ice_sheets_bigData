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
cmd = "docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cassandra-1"

find_ip = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
res = find_ip.coommunicate()[0]
res = res.decode("utf-8")
print(res)
raise SystemExit
class cassandraKeyspace:

    def __init__(self):
        pass  # call method to connecto to cluster in cassandra

def createKeySpace():
    time.sleep(5)
    cluster = Cluster(contact_points=['172.21.0.5'],port=9042)  # 172.21.0.6
    session = cluster.connect()

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

#createKeySpace()
