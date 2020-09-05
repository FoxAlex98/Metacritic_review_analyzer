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

def cleaner(message):
    data = json.loads(message)
    return data["review"]

sc = SparkContext(appName="Testing")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 1)

zkQuorum="10.0.100.22:2181"
topic = "numtest2"
kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {'numtest2': 1})


lines = kvs.map(lambda x: cleaner(x[1]))
count = lines.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)
count.pprint()

ssc.start()
ssc.awaitTermination()