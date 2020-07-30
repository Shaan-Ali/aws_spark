from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pykafka import KafkaClient
import json
import sys
import pprint

CHECKPOINT_DIR = "checkpoint/top10_airports"
OUTPUT_DIR = "intermediate/top10_airports/"
APP_NAME = "Top 10 Airports"


# Function to create and setup a new StreamingContext
def functionToCreateContext():
    conf = SparkConf()
    conf = conf.setAppName(APP_NAME)
    sc = SparkContext(conf=conf)

    # http://stackoverflow.com/questions/24686474/shipping-python-modules-in-pyspark-to-other-nodes
    # sc.addPyFile("common.py")

    # As argument Spark Context and batch retention
    ssc = StreamingContext(sc, 60)

    # set checkpoint directory
    ssc.checkpoint(CHECKPOINT_DIR)

    # return streaming spark context
    return ssc


def parse(rows):
    """Parse multiple rows"""
    return [parse_row(row) for row in rows]


zkQuorum, topic = sys.argv[1:]
ssc = StreamingContext.getOrCreate(CHECKPOINT_DIR, functionToCreateContext)
sc = ssc.sparkContext
kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})



# Get lines from kafka stream
ontime_data = kvs.map(lambda x: x[1]).map(lambda line: line.split(",")[2]).flatMap(parse)

# Get origin and destionation
origin = ontime_data.map(lambda x: (x.Origin, 1)).reduceByKey(lambda a, b: a + b)
dest = ontime_data.map(lambda x: (x.Dest, 1)).reduceByKey(lambda a, b: a + b)

# Union of the twd RDD. Sum by the same key. Then remember it
popular = origin.union(dest).reduceByKey(lambda a, b: a + b)

# traforming data using 1 as a key, and (AirlineID, ArrDelay) as value
popular2 = popular.map(lambda airport, count: (True, [(airport, count)]))

# Flat map values
airports = popular2.flatMapValues(lambda x: x).map(lambda key, value: value)

# debug
airports.pprint()

# Saving data in hdfs
airports.repartition(1).saveAsTextFiles(OUTPUT_DIR)


ssc.start()
ssc.awaitTermination()
