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
from langdetect import detect
from elasticsearch import Elasticsearch

global spark

es_write_conf = {
"es.nodes" : "10.0.100.51",
"es.port" : "9200",
"es.resource" : '%s/%s' % ("metacritic","_doc"),
"es.input.json" : "yes"
}

def get_review(_review):
    return {
            'name': _review['name'],
            'rating': _review['rating'],
            #'date': get_date(_review),
            'language': get_language(_review)
            #'review': _review['review']
            #'valid': get_valid()
            }

def get_date(review):
    try:
        date = review['date']
        return datetime.datetime.strptime(date, '%b %d, %Y')
    except TypeError as err:
        print("///////////////////////////")
        print(err)
        print("review " + str(review))
        return datetime.now()


def get_language(review):
    try:
        text = review['review']
        return detect(text)
    except TypeError as err:
        print("///////////////////////////")
        print(err)
        print("review " + str(review))
        return "NaN"

def message_processing(key, rdd):
    message = spark.read.json(rdd.map(lambda value: json.loads(value[1])))
    if not message.rdd.isEmpty():        
        analyzed_rdd = message.rdd.map(lambda review: get_review(review))
        print("\n\n\n\n") 
        print(spark.createDataFrame(analyzed_rdd).show())
        print("-----------------------------")

        #elastic search
        elastic_rdd = analyzed_rdd.map(lambda item: json.dumps(item)).map(lambda x: ('key', x))

        elastic_rdd.saveAsNewAPIHadoopFile(
            path='-',
            outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
            keyClass="org.apache.hadoop.io.NullWritable",
            valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
            conf=es_write_conf)  


mapping = {
    "mappings": {
        "properties": {
            "timestamp": {
                "type": "date"
            }
        }
    }
}

elastic = Elasticsearch(hosts=["10.0.100.51"])

response = elastic.indices.create(
    index="metacritic",
    body=mapping,
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