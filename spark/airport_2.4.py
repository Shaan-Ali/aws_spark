import sys
import time
import signal
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from common import *
from boto import dynamodb2
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item

n_secs = 1
topic = "order_data"
conf = SparkConf().setAppName("KafkaStreamProcessor").setMaster("local[*]")
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, n_secs)

ssc.checkpoint('~/dev/aws_spark/tmp/g2ex4')
AWS_REGION = 'us-east-2'
DB_TABLE = 't2g2ex4'
dynamo = dynamodb2.connect_to_region(AWS_REGION)
out_table = Table(DB_TABLE, connection = dynamo)

######
###### Partial results printer #######
######
def save_partition(part):
    for record in part:
        item = Item(out_table, data={
            "origin": record[0][0],
            "destination": record[0][1],
            "average_delay": int(record[1][0] / record[1][1])
        })
        item.save(overwrite=True)


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

filtered = ontime_data.map(lambda fl: ((fl.Origin, fl.Dest), (fl.ArrDelay, 1)))\
                .updateStateByKey(updateFunction)


# filtered.foreachRDD(lambda rdd: print_rdd(rdd))
filtered.foreachRDD(lambda rdd: rdd.foreachPartition(save_partition))

ssc.start()
# time.sleep(600) # Run stream for 10 minutes just in case no detection of producer # ssc. awaitTermination() ssc.stop(stopSparkContext=True,stopGraceFully=True)

try:
    ssc.awaitTermination()
except:
    pass

try:
    time.sleep(10)
except:
    pass