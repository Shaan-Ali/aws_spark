import sys
import time
import signal
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
ssc.checkpoint('~/dev/aws_spark/tmp/g2ex2')

def print_rdd(rdd):
    print('=============================')
    daysOfWeek = rdd.takeOrdered(10, key = lambda x: x[1][0]/x[1][1])
    for day in daysOfWeek:
        print('(' + str(day[0]) + ', ' + str(day[1][0] / day[1][1]) + ')')
    print('=============================')


def updateFunction(new_values, last_sum):

    new_vals0 = 0.0
    new_vals1 = 0

    for val in new_values:
        new_vals0 += val[0]
        new_vals1 += val[1]

    last_vals0 = last_sum[0] if last_sum is not None else 0.0
    last_vals1 = last_sum[1] if last_sum is not None else 0

    return (new_vals0 + last_vals0,\
            new_vals1 + last_vals1)


kafkaStream = KafkaUtils.createDirectStream(ssc,[topic], {
    'bootstrap.servers':'localhost:9092',
    'group.id':'video-group',
    'fetch.message.max.bytes':'15728640',
    'auto.offset.reset':'largest'}) # Group ID is completely arbitrary

ontime_data = kafkaStream.map(lambda x: x[1]).map(split).flatMap(parse)

filtered = ontime_data.map(lambda fl: ((fl.Origin, fl.Dest), (fl.DepDelay, 1)))\
                                      .updateStateByKey(updateFunction)


filtered.foreachRDD(lambda rdd: print_rdd(rdd))

# filtered.pprint()

ssc.start()
time.sleep(600) # Run stream for 10 minutes just in case no detection of producer # ssc. awaitTermination() ssc.stop(stopSparkContext=True,stopGraceFully=True)

