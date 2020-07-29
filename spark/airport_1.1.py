import sys
import time

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from common import *

n_secs = 1
topic = "order_data"
conf = SparkConf().setAppName("KafkaStreamProcessor").setMaster("local[*]")
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, n_secs)


kafkaStream = KafkaUtils.createDirectStream(ssc,[topic], {
    'bootstrap.servers':'localhost:9092',
    'group.id':'video-group',
    'fetch.message.max.bytes':'15728640',
    'auto.offset.reset':'largest'}) # Group ID is completely arbitrary

ontime_data = kafkaStream.map(lambda x: x[1]).map(split).flatMap(parse)

# Get origin and destionation
origin = ontime_data.map(lambda x: (x.Origin,1)).reduceByKey(lambda a, b: a+b)
dest = ontime_data.map(lambda x: (x.Dest,1)).reduceByKey(lambda a, b: a+b)

# Union of the twd RDD. Sum by the same key. Then remember it
popular = origin.union(dest).reduceByKey(lambda a, b: a+b)

# traforming data using 1 as a key, and (AirlineID, ArrDelay) as value
popular2 = popular.map(lambda (airport, count): (True, [(airport, count)]))

# Flat map values
airports = popular2.flatMapValues(lambda x: x).map(lambda (key, value): value)

# debug

airports.pprint()

ssc.start()
time.sleep(600) # Run stream for 10 minutes just in case no detection of producer # ssc. awaitTermination() ssc.stop(stopSparkContext=True,stopGraceFully=True)
