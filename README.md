In order to start the system 

From the root directory of the 


```
docker-compose -f producers/docker-compose.yml build
docker-compose -f consumers/caribou_split_processor/docker-compose.yml build
docker-compose -f manual_cass_sinks/docker-compose.yml build


```