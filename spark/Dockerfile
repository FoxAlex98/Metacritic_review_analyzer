FROM openjdk:8

ENV SPARK_VERSION "2.4.6"
ENV SPARK_DIR "/opt/spark"
ENV PATH $SPARK_DIR/bin:$PATH
ENV PATH "/root/.local/bin:$PATH"
ENV PATH "/opt/tap/code:$PATH"

RUN apt-get update && apt-get -y install python3.7 python3-pip wget

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYSPARK_DRIVER_PYTHON python3.7
ENV PYSPARK_PYTHON python3.7

ADD setup/spark-${SPARK_VERSION}-bin-hadoop2.7.tgz /opt

# Create Sym Link 
RUN ln -s /opt/spark-${SPARK_VERSION}-bin-hadoop2.7 ${SPARK_DIR} 

COPY setup/elasticsearch-hadoop-7.9.1.jar ${SPARK_DIR}/

COPY code/*  /opt/tap/code/

# Add Spark Starter
COPY spark-starter.sh $SPARK_DIR/bin/

WORKDIR ${SPARK_DIR}/bin
CMD ./spark-starter.sh

#COPY spark-starter.sh $SPARK_DIR/bin/spark-starter

#WORKDIR ${SPARK_DIR}
#ENTRYPOINT [ "bin/spark-starter" ]