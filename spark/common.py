import os
import csv
import datetime
from collections import namedtuple
from io import StringIO

ZOOKEEPER = ['localhost:2181']
ZKQUORUM = ",".join(ZOOKEEPER) #zkQuorum:  Zookeeper quorum (hostname:port,hostname:port,..)
# HDFS_PREFIX = "hdfs://%s:8020" %(HOST)
LOOKUP_DIR = "~/dev/ccc-capstone/lookup/"
DATA_DIR = "~/dev/ccc-capstone/filtered_data"
TEST_DIR = "~/dev/ccc-capstone/test"
DATE_FMT = "%Y-%m-%d"
# DATE_FMT = "%m/%d/%Y"
TIME_FMT = "%H%M"


# Those are my fields
fields = ("FlightDate", "Origin", "DepTime", "DepDelay", "Dest", "ArrTime", "ArrDelay",
            "DayOfWeek", "AirlineID", "Carrier", "FlightNum", "Year")
# 1/26/1988,LAS,35,16,ORD,546,20,2,19977,UA,500,1988

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
    # row[fields.index("FlightDate")] = datetime.datetime.strptime(row[fields.index("FlightDate")], DATE_FMT).date()
    # row[fields.index("Origin")] = str(row[fields.index("Origin")])
    # row[fields.index("DepTime")] = int(row[fields.index("DepTime")])
    # row[fields.index("DepDelay")] = int(row[fields.index("DepDelay")])
    # row[fields.index("Dest")] = str(row[fields.index("Dest")])
    # row[fields.index("ArrTime")] = int(row[fields.index("ArrTime")])
    # row[fields.index("ArrDelay")] = int(row[fields.index("ArrDelay")])
    # row[fields.index("DayOfWeek")] = int(row[fields.index("DayOfWeek")])
    # row[fields.index("AirlineID")] = int(row[fields.index("AirlineID")])
    # row[fields.index("Carrier")] = str(row[fields.index("Carrier")])
    # row[fields.index("FlightNum")] = int(row[fields.index("FlightNum")])
    # row[fields.index("Year")] = int(row[fields.index("Year")])


    row[fields.index("FlightDate")] = datetime.datetime.strptime(row[fields.index("FlightDate")], DATE_FMT).date()
    row[fields.index("Origin")] = str(row[fields.index("Origin")])
    row[fields.index("DepTime")] = float(row[fields.index("DepTime")])
    row[fields.index("DepDelay")] = float(row[fields.index("DepDelay")])
    row[fields.index("Dest")] = str(row[fields.index("Dest")])
    row[fields.index("ArrTime")] = float(row[fields.index("ArrTime")])
    row[fields.index("ArrDelay")] = float(row[fields.index("ArrDelay")])
    row[fields.index("DayOfWeek")] = float(row[fields.index("DayOfWeek")])
    row[fields.index("AirlineID")] = float(row[fields.index("AirlineID")])
    row[fields.index("Carrier")] = str(row[fields.index("Carrier")])
    row[fields.index("FlightNum")] = float(row[fields.index("FlightNum")])
    row[fields.index("Year")] = float(row[fields.index("Year")])

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

