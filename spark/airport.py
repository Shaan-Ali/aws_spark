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

# Those are my fields
fields = ("FlightDate", "AirlineID", "FlightNum", "Origin", "OriginCityName", "OriginStateName", "Dest", "DestCityName",
          "DestStateName", "CRSDepTime", "DepDelay", "CRSArrTime", "ArrDelay", "Cancelled", "CancellationCode",
          "Diverted", "CRSElapsedTime", "ActualElapsedTime", "AirTime", "Distance")

# A namedtuple object
Ontime = namedtuple('Ontime', fields)


def split(line):
    """Operator function for splitting a line with csv module"""
    reader = csv.reader(StringIO(line))
    return list(reader)


def splitOne(line):
    """Operator function for splitting a line with csv module"""
    reader = csv.reader(StringIO(line))
    return reader.next()


def parse(rows):
    """Parse multiple rows"""
    return [parse_row(row) for row in rows]


def parse_row(row):
    """Parses a row and returns a named tuple"""

    row[fields.index("FlightDate")] = datetime.datetime.strptime(row[fields.index("FlightDate")], DATE_FMT).date()
    row[fields.index("AirlineID")] = int(row[fields.index("AirlineID")])
    row[fields.index("FlightNum")] = int(row[fields.index("FlightNum")])

    # cicle amoung scheduled times
    for index in ["CRSDepTime", "CRSArrTime"]:
        if row[fields.index(index)] == "2400":
            row[fields.index(index)] = "0000"

        # Handle time values
        try:
            row[fields.index(index)] = datetime.datetime.strptime(row[fields.index(index)], TIME_FMT).time()

        except ValueError:
            # raise Exception, "problem in evaluating %s" %(row[fields.index(index)])
            row[fields.index(index)] = None

    row[fields.index("Cancelled")] = bool(int(row[fields.index("Cancelled")]))
    row[fields.index("Diverted")] = bool(int(row[fields.index("Diverted")]))

    # handle cancellation code
    if row[fields.index("CancellationCode")] == '"':
        row[fields.index("CancellationCode")] = None

    # `handle float values
    for index in ["DepDelay", "ArrDelay", "CRSElapsedTime", "Distance", "ActualElapsedTime", "AirTime"]:
        try:
            row[fields.index(index)] = float(row[fields.index(index)])
        except ValueError:
            row[fields.index(index)] = None

    return Ontime(*row)

def parse(rows):
    """Parse multiple rows"""
    return [parse_row(row) for row in rows]


kafkaStream = KafkaUtils.createDirectStream(ssc,[topic], {
    'bootstrap.servers':'localhost:9092',
    'group.id':'video-group',
    'fetch.message.max.bytes':'15728640',
    'auto.offset.reset':'largest'}) # Group ID is completely arbitrary

# lines = kafkaStream.map(lambda x: x[1])
# counts = lines.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)

# Get lines from kafka stream
ontime_data = kafkaStream.map(lambda x: x[1]).map(lambda line: line.split(",")[2]).flatMap(parse)

# Get origin and destionation
origin = ontime_data.map(lambda x: (x.Origin, 1)).reduceByKey(lambda a, b: a + b)
dest = ontime_data.map(lambda x: (x.Dest, 1)).reduceByKey(lambda a, b: a + b)

# Union of the twd RDD. Sum by the same key. Then remember it
popular = origin.union(dest).reduceByKey(lambda a, b: a + b)

# traforming data using 1 as a key, and (AirlineID, ArrDelay) as value
popular2 = popular.map(lambda airport, count: (True, [(airport, count)]))

# Flat map values
airports = popular2.flatMapValues(lambda x: x).map(lambda key, value: value)



airports.pprint()

ssc.start()
time.sleep(600) # Run stream for 10 minutes just in case no detection of producer # ssc. awaitTermination() ssc.stop(stopSparkContext=True,stopGraceFully=True)
