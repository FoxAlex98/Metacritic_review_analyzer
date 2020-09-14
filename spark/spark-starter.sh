#!/bin/bash
./spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.6,org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.6 /opt/tap/code/stream.py