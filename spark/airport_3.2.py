import sys
import time
import signal
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from common import *

n_secs = 1
topic = "order_data"

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

#  flight_date = datetime.date(flight.Year, flight.Month, flight.DayofMonth)
# AttributeError: 'Ontime' object has no attribute 'Month'

def map_flight(flight, is_yz=False):
    flight_date = datetime.date(flight.FlightDate)
    y_flight = flight.Dest
    if (is_yz):
        flight_date -= datetime.timedelta(days=2)
        y_flight = flight.Origin
    return ((str(flight_date), y_flight), flight)


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
flights_xy = ontime_data.filter(lambda fl: fl.DepTime < "1200")\
                .map(map_flight)
                #.reduceByKey(reduce_flight)

# filter YZ candidates
flights_yz = ontime_data.filter(lambda fl: fl.DepTime > "1200")\
                .map(lambda fl: map_flight(fl, True))
                #.reduceByKey(reduce_flight)

# join both legs
flights_xyz = flights_xy.join(flights_yz)


flights_xyz.foreachRDD(lambda rdd: print_rdd(rdd))


ssc.start()
time.sleep(600) # Run stream for 10 minutes just in case no detection of producer # ssc. awaitTermination() ssc.stop(stopSparkContext=True,stopGraceFully=True)

# https://github.com/gmcorral/cloud-capstone/blob/master/spark/flight.py