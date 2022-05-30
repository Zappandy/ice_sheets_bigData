from cassandra.cluster import Cluster

cluster = Cluster(["cassandra-1"])
session = cluster.connect()
session.set_keyspace("icesheet_keyspace")
rows = session.execute('SELECT * FROM icesheetreport;')


