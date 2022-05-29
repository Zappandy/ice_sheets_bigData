#!/bin/sh


echo "Starting Icesheets Sink"
curl -s \
     -X POST "http://localhost:8083/connectors" \
     -H "Content-Type: application/json" \
     -d '{
  "name": "cass_json_sink",
  "config":{
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",  
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable":"false",
    "tasks.max": "10",
    "topics": "icesheets",
    "contactPoints": "cassandra-1",
    "loadBalancing.localDc": "datacenter1",
    "topic.icesheets.icesheet_keyspace.icesheetreport.mapping": "Year=value.Year, Month=value.Month, Day=value.Day, Hemisphere=key.Hemisphere, Extent=value.Extent, Missing=value.Missing",
    "topic.icesheets.icesheet_keyspace.icesheetreport.consistencyLevel": "LOCAL_QUORUM"
  }
}'
echo "Done."
