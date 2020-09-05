from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json

sc = SparkContext(appName="Testing")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 1)

zkQuorum="10.0.100.22:2181"
topic = "numtest2"
kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {'numtest2': 1})

lines = kvs.map(lambda x: x[1])

lines.pprint()

ssc.start()
ssc.awaitTermination()