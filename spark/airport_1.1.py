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
ssc.checkpoint('~/dev/aws_spark/tmp/g1ex1')

######
###### Partial results printer #######
######
def print_rdd(rdd):
    print('=============================')
    airports = rdd.takeOrdered(10, key = lambda x: -x[1])
    for airport in airports:
        print(airport)
    print('=============================')


######
###### Checkpoint status updater #######
######
def updateFunction(new_values, last_sum):
    return sum(new_values) + (last_sum or 0)


kafkaStream = KafkaUtils.createDirectStream(ssc,[topic], {
    'bootstrap.servers':'localhost:9092',
    'group.id':'video-group',
    'fetch.message.max.bytes':'15728640',
    'auto.offset.reset':'largest'}) # Group ID is completely arbitrary

# Main Code
ontime_data = kafkaStream.map(lambda x: x[1]).map(split).flatMap(parse)

filtered = ontime_data.flatMap(lambda fl: [(fl.Origin, 1), (fl.Dest, 1)])\
                                      .updateStateByKey(updateFunction)

filtered.foreachRDD(lambda rdd: print_rdd(rdd))

# start streaming process
ssc.start()

try:
    ssc.awaitTermination()
except:
    pass

try:
    time.sleep(10)
except:
    pass