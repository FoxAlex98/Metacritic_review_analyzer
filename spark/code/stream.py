import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

spark = SparkSession\
        .builder\
        .appName("StructuredKafkaWordCount")\
        .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

    # Create DataSet representing the stream of input lines from kafka
lines = spark\
        .readStream\
        .format("kafka")\
        .option("startingOffsets","earliest")\
        .option("kafka.bootstrap.servers", "10.0.100.23:9092")\
        .option("subscribe", "numtest2")\
        .load()\
        .selectExpr("CAST(value AS STRING)")

    # Split the lines into words
words = lines.select(explode(split(lines.value, ' ')).alias('word'))

    # Generate running word count
wordCounts = words.groupBy('word').count()

    # Start running the query that prints the running counts to the console
query = wordCounts\
           .writeStream\
           .outputMode('complete')\
           .format('console')\
           .start()

query.awaitTermination()