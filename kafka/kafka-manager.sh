#!/bin/bash
ZK_DATA_DIR=/tmp/zookeeper
ZK_SERVER="localhost"
[[ -z "${KAFKA_ACTION}" ]] && { echo "KAFKA_ACTION required"; exit 1; }
[[ -z "${KAFKA_DIR}" ]] && { echo "KAFKA_DIR missing"; exit 1; }
# ACTIONS start-zk, start-kafka, create-topic, 

echo "Running action ${KAFKA_ACTION} (Kakfa Dir:${KAFKA_DIR}, ZK Server: ${ZK_SERVER})"
case ${KAFKA_ACTION} in
"start-kafka")
cd ${KAFKA_DIR}
kafka-server-start.sh config/server.properties
;;
"create-topic")
cd ${KAFKA_DIR}
kafka-topics.sh --create --zookeeper 10.0.100.22:2181 --replication-factor 1 --partitions 1 --topic ${KAFKA_TOPIC}
;;
"producer")
cd ${KAFKA_DIR}
#bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
kafka-console-producer.sh --broker-list 10.0.100.23:9092 --topic ${KAFKA_TOPIC}
;;
"consumer")
cd ${KAFKA_DIR}
kafka-console-consumer.sh --bootstrap-server 10.0.100.23:9092 --topic ${KAFKA_TOPIC} --from-beginning ${KAFKA_CONSUMER_PROPERTIES}
;;
esac

