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

global spark

def get_review(_review):
    return {
            'name': _review['name'],
            'rating': int(_review['rating']),
            'date': get_date(_review['date']).date(),
            #'review': _review['review']
        }

def get_date(date):
    return datetime.datetime.strptime(date, '%b %d, %Y')

def message_processing(key, rdd):
    message = spark.read.json(rdd.map(lambda value: json.loads(value[1])))
    if not message.rdd.isEmpty():        
        analyzed_rdd = message.rdd.map(lambda review: get_review(review))
        print("\n\n\n\n") 
        print(spark.createDataFrame(analyzed_rdd).show())
    #elastic search

spark = SparkSession.builder.appName("Testing").getOrCreate()
spark.sparkContext.setLogLevel("WARN")
ssc = StreamingContext(spark.sparkContext, 3)

zkQuorum="10.0.100.22:2181"
topic = "numtest2"
kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {'numtest2': 1})

kvs.foreachRDD(message_processing)

ssc.start()
ssc.awaitTermination()