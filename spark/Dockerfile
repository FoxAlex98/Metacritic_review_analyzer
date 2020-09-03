FROM openjdk:8-jre

ENV PATH $SPARK_DIR/bin:$PATH
ENV SPARK_VERSION=2.4.6
ENV SPARK_DIR=/opt/spark
ENV PATH $SPARK_DIR/bin:$PATH

ADD setup/spark-${SPARK_VERSION}-bin-hadoop2.7.tgz /opt

RUN apt-get update && apt-get -y install bash python python-pip

RUN pip install pyspark numpy elasticsearch kafka-python
# Create Sym Link 
RUN ln -s /opt/spark-${SPARK_VERSION}-bin-hadoop2.7 ${SPARK_DIR} 

ADD code/*  /opt/tap/
# Add Spark Manager
ADD spark-starter.sh $SPARK_DIR/bin/spark-starter

WORKDIR ${SPARK_DIR}
ENTRYPOINT [ "bin/spark-starter" ]