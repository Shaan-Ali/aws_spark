from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pykafka import KafkaClient
import json
import sys
import pprint


zkQuorum, topic = sys.argv[1:]
sc = SparkContext("local[2]", "KafkaOrderCount")
ssc = StreamingContext(sc, 10)
kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})


def parseLine(line):
    fields = line.split(',')
    arrDelay = float(fields[6])
    carrier = fields[9]
    return (carrier, arrDelay)


# lines = sc.textFile("file:///SparkCourse/capstone/On_Time_On_Time_Performance_1988_1.csv")
rdd = kvs.map(parseLine)

# totalsByAge = rdd.mapValues(lambda x: (x, 1)).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
arrDelayTotalByCarrier = rdd.mapValues(lambda x: (x, 1)).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))

# averagesByAge = totalsByAge.mapValues(lambda x: x[0] / x[1])
avgDelay = arrDelayTotalByCarrier.mapValues(lambda x: x[0] / x[1]).collect()
# results = avgDelay.sortBy(lambda a: a[1]).collect()

# results = sorted(avgDelay.sortBy(lambda a: a[1]).collect())
for result in results:
    print(result)


status_count.pprint()
ssc.start()
ssc.awaitTermination()
