from cassandra.cluster import Cluster
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

cluster = Cluster(["cassandra-1"])
session = cluster.connect()
session.set_keyspace("icesheet_keyspace")

def df_generator(cols, rows):
    return pd.DataFrame(rows, columns=cols)

session.row_factory = df_generator
session.default_fetch_size = None

ice_sheetrows = session.execute('SELECT * FROM icesheetreport;')
ice_df = ice_sheetrows._current_rows
caribou_sheetrows = session.execute('SELECT * FROM cariboureport;')
caribou_df = caribou_sheetrows._current_rows
oceanheat_sheetrows = session.execute('SELECT * FROM oceanheatreport;')
oceanheat_df = oceanheat_sheetrows._current_rows
globaltemp_sheetrows = session.execute('SELECT * FROM globaltempreport;')
globaltemp_df = globaltemp_sheetrows._current_rows

mask_ice_df = ice_df["Hemisphere"] == 'S'
viz_ice_df = ice_df[mask_ice_df]
lis_year = viz_ice_df["Year"]
lis_extent = viz_ice_df["Extent"]
#mask_ice_df["Mony
plt.scatter(lis_year, lis_extent)
plt.show()
#ice_sheet_south = session.execute('SELECT * FROM icesheetreport where \"Hemisphere\" = S and \"Month\" = 7;')



