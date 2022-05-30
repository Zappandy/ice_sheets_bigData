echo "taking down containers"
docker-compose -f producers/docker-compose.yml down
docker-compose -f consumers/caribou_split_processor/docker-compose.yml down
docker-compose -f manual_cass_sinks/docker-compose.yml down

# building other containers
echo "building other containers"
docker-compose -f producers/docker-compose.yml build
docker-compose -f consumers/caribou_split_processor/docker-compose.yml build
docker-compose -f manual_cass_sinks/docker-compose.yml build

echo "buildig / starting producers"
docker-compose -f producers/docker-compose.yml up -d

echo "building / starting processors"
docker-compose -f consumers/caribou_split_processor/docker-compose.yml up -d

echo "building / starting sinks"
docker-compose -f manual_cass_sinks/docker-compose.yml up -d