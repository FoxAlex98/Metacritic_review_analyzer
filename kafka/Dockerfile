FROM maven:latest
ENV PATH /opt/kafka/bin:$PATH
ENV KAFKA_DIR "/opt/kafka"
ENV ZOOKEEPER_SERVER "10.0.100.22:2181"
ENV MCREVIEWS_CONNECTOR "MCReviews-Connector"
ENV MCREVIEWS_SETUP "Kafka-Setup"
ENV MCREVIEWS_CONNECT_DIR "/opt/connector"
ENV KAFKA_PLUGINS_DIR "/usr/local/share/kafka/plugins/"
ARG KAFKA_VERSION="2.12-2.5.0"

# Installing Kafka
ADD ${MCREVIEWS_SETUP}/kafka_${KAFKA_VERSION}.tgz /opt
# Create Sym Link 
RUN ln -s /opt/kafka_${KAFKA_VERSION} ${KAFKA_DIR} 
#Copy properties
COPY ${MCREVIEWS_SETUP}/source-setup.properties ${KAFKA_DIR}/conf/
COPY ${MCREVIEWS_SETUP}/worker.properties ${KAFKA_DIR}/conf/
COPY ${MCREVIEWS_SETUP}/MCReviews-Connector-0.0.1-SNAPSHOT.jar ${KAFKA_PLUGINS_DIR}
COPY ${MCREVIEWS_SETUP}/kafka-starter.sh ${KAFKA_DIR}

WORKDIR ${KAFKA_DIR}
CMD ./kafka-starter.sh