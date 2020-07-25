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

lines = kvs.map(lambda x: x[1])
status_count = lines.map(lambda line: line.split(",")[2]) \
              .map(lambda order_status: (order_status, 1)) \
              .reduceByKey(lambda a, b: a+b)


status_count.pprint()
status_count.pprint()
ssc.start()
ssc.awaitTermination()
