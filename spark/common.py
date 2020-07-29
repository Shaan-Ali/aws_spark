import os
import csv
import datetime
from collections import namedtuple
from StringIO import StringIO

ZOOKEEPER = ['localhost:2181']
ZKQUORUM = ",".join(ZOOKEEPER) #zkQuorum:  Zookeeper quorum (hostname:port,hostname:port,..)
# HDFS_PREFIX = "hdfs://%s:8020" %(HOST)
LOOKUP_DIR = "~/dev/ccc-capstone/lookup/"
DATA_DIR = "~/dev/ccc-capstone/filtered_data"
TEST_DIR = "~/dev/ccc-capstone/test"
# DATE_FMT = "%Y-%m-%d"
DATE_FMT = "%m/%d/%Y"
TIME_FMT = "%H%M"


# Those are my fields
# fields = ("FlightDate", "AirlineID", "FlightNum", "Origin", "OriginCityName", "OriginStateName", "Dest", "DestCityName",
#           "DestStateName", "CRSDepTime", "DepDelay", "CRSArrTime", "ArrDelay", "Cancelled", "CancellationCode",
#           "Diverted", "CRSElapsedTime", "ActualElapsedTime", "AirTime", "Distance")

fields = ("FlightDate", "Origin", "DepTime", "DepDelay", "Dest", "ArrTime", "ArrDelay",
            "DayOfWeek", "AirlineID", "Carrier", "FlightNum", "Year")

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
#     row[fields.index("FlightDate")] = str("1/1/1988")
    row[fields.index("AirlineID")] = int(row[fields.index("AirlineID")])
    row[fields.index("FlightNum")] = int(row[fields.index("FlightNum")])

#     # cicle amoung scheduled times
#     for index in ["DepTime", "ArrTime"]:
#         if row[fields.index(index)] == "2400":
#             row[fields.index(index)] = "0000"

#         # Handle time values
#         try:
#             row[fields.index(index)] = datetime.datetime.strptime(row[fields.index(index)], TIME_FMT).time()
#
#         except ValueError:
#             # raise Exception, "problem in evaluating %s" %(row[fields.index(index)])
#             row[fields.index(index)] = None

    # handle cancellation code
#     if row[fields.index("CancellationCode")] == '"':
#         row[fields.index("CancellationCode")] = None

    return Ontime(*row)

