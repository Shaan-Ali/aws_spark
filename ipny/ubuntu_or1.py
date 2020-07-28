import findspark # TODO: your path will likely not have 'matthew' in it. Change it to reflect your path.
findspark.init('home/matthew/spark-2.3.0-bin-hadoop2.7')
import os
os.environ['PYSPARK_SUBMIT_ARGS1'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.0 pyspark-shell'
import sys
import time
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

n_secs = 1
topic = "pyspark-kafka-demo"
conf = SparkConf().setAppName("KafkaStreamProcessor").setMaster("local[*]")
sc = SparkContext(conf=conf) sc.setLogLevel("WARN")
ssc = StreamingContext(sc, n_secs)

11°   kAfkActrom, = rroatalirortGtroamf.. itnnirl { 'bootstrap.servers':'localhost:9092', 'group.id':'video-group', 'fetch.message.max.bytes':'15728640', 'auto.offset.reset':'largest'l) # Group ID is completely arbitrary

lines = kvs.map(lambda x: x[1]) counts = lines.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)

counts.pprint()
ssc.start() time.sleep(600) # Run stream for 10 minutes just in case no detection of producer # ssc. awaitTermination() ssc.stop(stopSparkContext=True,stopGraceFully=True)
