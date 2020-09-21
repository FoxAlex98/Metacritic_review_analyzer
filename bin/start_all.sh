echo "starting zookeeper"
docker-compose up -d zookeeper

sleep 8s

echo "starting kafka server"
docker-compose up -d kafka

sleep 8s

echo 'starting ES and kibana'
docker-compose up -d elasticsearch kibana

sleep 3

echo 'waiting for kafka to start spark'
cd spark/bin
bash ./start.sh

echo 'waiting for spark ...'

sleep 8s

echo 'All is Ready. Please run scraper'