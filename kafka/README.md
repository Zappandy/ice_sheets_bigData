# Connections

run 
```sh
docker exec -it connect_1
```

see if connection is okay by running
```sh
curl -X POST -H "Content-Type: application/json" -d "@/etc/kafka-connect/connectors/basic_connect.json" "http://localhost:8083/connectors"
```
