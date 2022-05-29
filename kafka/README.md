# Connections

run 
```sh
docker exec -it datastax-connect bash
```

see if connection is okay by running
```sh
curl -X POST -H "Content-Type: application/json" -d "@/etc/kafka-connect/connectors/datastax_json_connect.json" "http://localhost:8083/connectors"
```
then...
```
curl -X GET "http://localhost:8083/connectors/cass_json_sink/status"
```
