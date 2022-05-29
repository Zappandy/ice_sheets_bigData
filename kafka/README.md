# Connections

run 
```sh
docker exec -it connect_1 bash
```

see if connection is okay by running
```sh
curl -X POST -H "Content-Type: application/json" -d "@/etc/kafka-connect/connectors/json_connect.json" "http://localhost:8083/connectors"
```
then...
```
curl -X GET "http://localhost:8083/connectors/cassandra-json-sink/status"
```
