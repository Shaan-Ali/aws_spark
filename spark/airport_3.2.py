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

AWS_REGION = 'us-east-2'
DB_TABLE = 't2g3ex2'
dynamo = dynamodb2.connect_to_region(AWS_REGION)
out_table = Table(DB_TABLE, connection = dynamo)

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

#  flight_date = datetime.date(flight.Year, flight.Month, flight.DayofMonth)
# AttributeError: 'Ontime' object has no attribute 'Month'


######
###### Mapper and reducer functions for XY flights #######
######
def map_flight(flight, is_yz=False):
    flight_date = flight.FlightDate
    y_flight = flight.Dest
    if (is_yz):
        flight_date -= datetime.timedelta(days=2)
        y_flight = flight.Origin
    return ((str(flight_date), y_flight), flight)

def reduce_flight(fl1, fl2):
    fl1_delay = fl1.DepDelay + fl1.ArrDelay
    fl2_delay = fl2.DepDelay + fl2.ArrDelay
    return fl1 if fl1_delay <= fl2_delay else fl2


######
###### Partial results printer #######
######
def save_partition(part):

    for record in part:
        fl_xy = record[1][0]
        fl_yz = record[1][1]
        route = fl_xy.Origin + '-' + fl_xy.Dest + '-' + fl_yz.Dest
        depdate = record[0][0]
        item_new = Item(out_table, data={
            "route": route,
            "depdate": depdate,
            "flight_xy": fl_xy.Carrier + str(fl_xy.FlightNum),
            "xy_delay": int(fl_xy.DepDelay + fl_xy.ArrDelay),
            "flight_yz": fl_yz.Carrier + str(fl_yz.FlightNum),
            "yz_delay": int(fl_yz.DepDelay + fl_yz.ArrDelay)
        })

        # check old item delay
        try:
            item_old = out_table.get_item(route=route, depdate = depdate)
            if (item_old['total_delay'] > item_new['total_delay']):
                item_new.save(overwrite=True)
        except:
            item_new.save(overwrite=True)


# ====================================
conf = SparkConf().setAppName("KafkaStreamProcessor").setMaster("local[*]")
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, n_secs)
ssc.checkpoint('~/dev/aws_spark/tmp/g3ex2')

kafkaStream = KafkaUtils.createDirectStream(ssc,[topic], {
    'bootstrap.servers':'localhost:9092',
    'group.id':'video-group',
    'fetch.message.max.bytes':'15728640',
    'auto.offset.reset':'largest'}) # Group ID is completely arbitrary


ontime_data = kafkaStream.map(lambda x: x[1]).map(split).flatMap(parse)

# filter XY candidates
flights_xy = ontime_data.filter(lambda fl: fl.DepTime < 1200)\
                .map(map_flight)
#                 .reduceByKey(reduce_flight)

# filter YZ candidates
flights_yz = ontime_data.filter(lambda fl: fl.DepTime > 1200)\
                .map(lambda fl: map_flight(fl, True)).reduceByKey(reduce_flight)

# join both legs
flights_xyz = flights_xy.join(flights_yz)


# flights_xyz.foreachRDD(lambda rdd: print_rdd(rdd))
flights_xyz.foreachRDD(lambda rdd: rdd.foreachPartition(save_partition))


ssc.start()

try:
    ssc.awaitTermination()
except:
    pass

try:
    time.sleep(10)
except:
    pass
