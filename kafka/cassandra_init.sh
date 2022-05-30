#!/bin/bash
set -e

#TBT="CREATE TABLE icesheetreport(_year INT, _month INT, _day INT, extend FLOAT, missing FLOAT, hemisphere TEXT) PRIMARY KEY (hemisphere, extend);"
# primary key is to identify a row
#the drop statement is here to store data for every stream, improve CQL command via python to simply add data per every new run
# although unneeded for this problem
CQL="DROP KEYSPACE IF EXISTS icesheet_keyspace;
     CREATE KEYSPACE icesheet_keyspace
     WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};
     USE icesheet_keyspace;
     CREATE TABLE icesheetreport(\"rec_id\" UUID PRIMARY KEY, \"Year\" INT, \"Month\" INT, \"Day\" INT,
     \"Extent\" FLOAT, \"Missing\" FLOAT, \"Hemisphere\" TEXT);
     CREATE TABLE cariboureport(\"rec_id\" UUID PRIMARY KEY, \"Year\" INT, location TEXT, population_count FLOAT);
     CREATE TABLE oceanheatreport(\"rec_id\" UUID PRIMARY KEY, year FLOAT, wo FLOAT, wose FLOAT, nh FLOAT, nhse FLOAT, sh FLOAT, shse FLOAT);
     CREATE TABLE globaltempreport(\"rec_id\" UUID PRIMARY KEY, year INT, no_smoothing FLOAT, lowess_smoothing FLOAT);
     "
until echo $CQL | cqlsh; do
	  echo "cqlsh: Cassandra is unavailable to initialize - will retry later"
	    sleep 2
    done &

    exec /custom_entrypoint.sh "$@"
