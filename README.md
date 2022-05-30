# How to set up the system

Run all the docker commands from the root directory of the repository


```
docker network create kafka-network 
```

Build all the containers. The visualization is not functional, so it does not need to be built and started.
```
docker-compose -f kafka/docker-compose.yml build
docker-compose -f producers/docker-compose.yml build
docker-compose -f consumers/caribou_split_processor/docker-compose.yml build
docker-compose -f consumers/ice_sheets_predictor/docker-compose.yml build
docker-compose -f manual_cass_sinks/docker-compose.yml build
(docker-compose-f visualization/docker-compose build)
```
This can take a while as the data sources are downloaded to the images when building.

First, start the message broker and the database by running

```
docker-compose -f kafka/docker-compose.yml run -d 
```
Sometimes the message broker container does not start up correctly. Simply run
check if it is running
```
docker ps
docker-compose -f kafka/docker-compose.yml run -d broker init-kafka
```
again and it should start up without problems.
Wait a couple of minutes, until everything is running (cassandra is slow to start up)

Finally, set up the other components of the stream processing system
```
docker-compose -f consumers/caribou_split_processor/docker-compose.yml run -d
docker-compose -f consumers/ice_sheets_predictor/docker-compose.yml run -d
docker-compose -f manual_cass_sinks/docker-compose.yml run -d
docker-compose -f producers/docker-compose.yml run -d
```

The producers start streaming messages immediately on startup.

If you want to control the producers, there is a control topic registered with kafka.
By sending commands to this topic, the producers can be stopped and their speed can be adjusted:
Some example commands are listed in the README under the producers directory: ![producers/README.md].
In order to use them, run a local kafka-console-producer and send the JSON commands to the "control" topic.
