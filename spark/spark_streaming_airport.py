from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pykafka import KafkaClient
import json
import sys
import pprint

OUTPUT_DIR = "intermediate/top10_airports/"

zkQuorum, topic = sys.argv[1:]
sc = SparkContext("local[2]", "KafkaOrderCount")
ssc = StreamingContext(sc, 10)
kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})


# Get lines from kafka stream
ontime_data = kvs.map(lambda x: x[1]).map(split).flatMap(parse)

# Get origin and destionation
origin = ontime_data.map(lambda x: (x.Origin, 1)).reduceByKey(lambda a, b: a + b)
dest = ontime_data.map(lambda x: (x.Dest, 1)).reduceByKey(lambda a, b: a + b)

# Union of the twd RDD. Sum by the same key. Then remember it
popular = origin.union(dest).reduceByKey(lambda a, b: a + b)

# traforming data using 1 as a key, and (AirlineID, ArrDelay) as value
popular2 = popular.map(lambda (airport, count): (True, [(airport, count)]))

# Flat map values
airports = popular2.flatMapValues(lambda x: x).map(lambda (key, value): value)

# debug
airports.pprint()

# Saving data in hdfs
airports.repartition(1).saveAsTextFiles(OUTPUT_DIR)


status_count.pprint()
ssc.start()
ssc.awaitTermination()
