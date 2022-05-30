# stop everything
echo "stoping all containers"
docker stop $(docker ps -q)

echo "building streaming backbone"
docker-compose -f kafka/docker-compose.yml build
docker-compose -f kafka/docker-compose.yml up -d

# building other containers
echo "building other containers"
docker-compose -f producers/docker-compose.yml build
docker-compose -f consumers/caribou_split_processor/docker-compose.yml build
docker-compose -f consumers/ice_sheets_predictor/docker-compose.yml build
docker-compose -f manual_cass_sinks/docker-compose.yml build


# TODO check for broker started
# TODO check for cassandra started
echo "waiting for cassandra and broker to spin up"
sleep 120
echo "let's continue"

echo "building / starting processors"
docker-compose -f consumers/caribou_split_processor/docker-compose.yml up -d
docker-compose -f consumers/ice_sheets_predictor/docker-compose.yml up -d

echo "building / starting sinks"
docker-compose -f manual_cass_sinks/docker-compose.yml up -d

echo "buildig / starting producers"
docker-compose -f producers/docker-compose.yml up -d

