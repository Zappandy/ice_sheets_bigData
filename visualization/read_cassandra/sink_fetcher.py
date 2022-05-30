from cassandra.cluster import Cluster

cluster = Cluster(["cassandra-1"])
session = cluster.connect()
session.set_keyspace("icesheet_keyspace")
ice_sheetrows = session.execute('SELECT * FROM icesheetreport;')
caribou_sheetrows = session.execute('SELECT * FROM cariboureport;')
oceanheat_sheetrows = session.execute('SELECT * FROM oceanheatreport;')
globaltemp_sheetrows = session.execute('SELECT * FROM globaltempreport;')

#"SELECT \"Hemisphere\" 

#ice_sheet_hemisphere = session.execute('SELECT \"Hemisphere\" FROM icesheetreport;')
ice_sheet_hemisphere = session.execute('SELECT * FROM icesheetreport where \"Hemisphere\" = S;')
    



