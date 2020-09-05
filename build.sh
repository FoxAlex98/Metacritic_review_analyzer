echo "Start MC Analizer..."

docker-compose stop

docker-compose up -d zookeeper

echo "waiting 5 seconds for kafka"
sleep 5s

docker-compose up -d kafka

echo "waiting 5 seconds for spark"
sleep 5s

docker-compose up spark
