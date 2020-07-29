import sys
import time
from operator import add
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

# filter out cancelled or diverted data: http://spark.apache.org/examples.html
# arrived_data = ontime_data.filter(lambda x: x.Cancelled is False and x.Diverted is False and x.AirlineID is not None and x.ArrDelay is not None)

# map by arrived delays
ArrDelay = ontime_data.map(lambda m: ((m.AirlineID, str(m.AirlineID)), m.ArrDelay))

# sum elements and number of elements, to store them in a intermediate file (k, (sum(v), len(v)))
collectDelays = ArrDelay.map(lambda (key, value): (key, [value])).reduceByKey(add).map(lambda (key, values): (key, [sum(values), len(values)]))

#debug
collectDelays.pprint()


ssc.start()
time.sleep(600) # Run stream for 10 minutes just in case no detection of producer # ssc. awaitTermination() ssc.stop(stopSparkContext=True,stopGraceFully=True)
