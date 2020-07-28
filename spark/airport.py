import sys
import time
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

n_secs = 1
topic = "order_data"
conf = SparkConf().setAppName("KafkaStreamProcessor").setMaster("local[*]")
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, n_secs)

def parseLine(line):
    fields = line.split(',')
    arrDelay = float(fields[6])
    carrier = fields[9]
    return (carrier, arrDelay)

def print_rdd(rdd):
    print('=============================')
    airports = rdd.takeOrdered(10, key = lambda x: -x[1])
    for airport in airports:
        print(airport)
    print('=============================')


kafkaStream = KafkaUtils.createDirectStream(ssc,[topic], {
    'bootstrap.servers':'localhost:9092',
    'group.id':'video-group',
    'fetch.message.max.bytes':'15728640',
    'auto.offset.reset':'largest'}) # Group ID is completely arbitrary

# lines = kafkaStream.map(lambda x: x[1])
# counts = lines.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)

# Get lines from kafka stream

rdd = kafkaStream.map(parseLine)

# totalsByAge = rdd.mapValues(lambda x: (x, 1)).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
arrDelayTotalByCarrier = rdd.mapValues(lambda x: (x, 1)).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))

# averagesByAge = totalsByAge.mapValues(lambda x: x[0] / x[1])
avgDelay = arrDelayTotalByCarrier.mapValues(lambda x: x[0] / x[1])
results = avgDelay.sortBy(lambda a: a[1]).collect()

# results = sorted(avgDelay.sortBy(lambda a: a[1]).collect())
# for result in results:
#     print(result)





results.pprint()

ssc.start()
time.sleep(600) # Run stream for 10 minutes just in case no detection of producer # ssc. awaitTermination() ssc.stop(stopSparkContext=True,stopGraceFully=True)
