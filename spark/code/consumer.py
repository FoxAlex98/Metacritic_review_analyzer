from __future__ import print_function

import sys
import os
import pyspark
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import Row
import json
import datetime
from elasticsearch import Elasticsearch
import data_extractors as dext
import configuration as conf

global spark

def message_processing(key, rdd):
    message = spark.read.option("mode", "DROPMALFORMED").json(rdd.map(lambda value: json.loads(value[1])))
    if not message.rdd.isEmpty():        
        analyzed_rdd = message.rdd.map(lambda review: dext.get_review(review))
        print("\n\n\n\n") 
        print(spark.createDataFrame(analyzed_rdd).show())
        print("-----------------------------")

        #elastic search
        elastic_rdd = analyzed_rdd.map(lambda item: json.dumps(item, default=conf.enco)).map(lambda x: ('key', x))

        elastic_rdd.saveAsNewAPIHadoopFile(
            path='-',
            outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
            keyClass="org.apache.hadoop.io.NullWritable",
            valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
            conf=conf.es_write_conf)  


elastic = Elasticsearch(hosts=["10.0.100.51"])

response = elastic.indices.create(
    index="metacritic",
    body=conf.mapping,
    ignore=400
)

    # elasticsearch index response
if 'acknowledged' in response:
    if response['acknowledged'] == True:
        print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])
elif 'error' in response:
    print ("ERROR:", response['error']['root_cause'])
    print ("TYPE:", response['error']['type'])



spark = SparkSession.builder.appName("Testing").getOrCreate()
spark.sparkContext.setLogLevel("WARN")
ssc = StreamingContext(spark.sparkContext, 3)

zkQuorum="10.0.100.22:2181"
topic = "numtest2"
kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {'numtest2': 1})

kvs.foreachRDD(message_processing)

ssc.start()
ssc.awaitTermination()