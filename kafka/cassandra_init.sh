#!/bin/bash
set -e

#TBT="CREATE TABLE icesheetreport(_year INT, _month INT, _day INT, extend FLOAT, missing FLOAT, hemisphere TEXT) PRIMARY KEY (hemisphere, extend);"
# primary key is to identify a row
#CQL="CREATE KEYSPACE IF NOT EXISTS icesheet_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};"
CQL="CREATE KEYSPACE IF NOT EXISTS icesheet_keyspace
     WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};
     USE icesheet_keyspace;
     CREATE TABLE IF NOT EXISTS icesheetreport(year INT, month INT, day INT,
     extend FLOAT, missing FLOAT, hemisphere TEXT, PRIMARY KEY (hemisphere));
     "
until echo $CQL | cqlsh; do
	  echo "cqlsh: Cassandra is unavailable to initialize - will retry later"
	    sleep 2
    done &

    exec /custom_entrypoint.sh "$@"
