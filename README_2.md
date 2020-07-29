# Cloud computing capstone - Part 2

## Testing Kafka installation

Inspect `/usr/hdp/current/kafka-broker/config/server.properties` for *zookeper* and
*listener* addresses:

```
$ grep ip-172-31-29-45.eu-central-1.compute.internal /usr/hdp/current/kafka-broker/config/server.properties                
listeners=PLAINTEXT://ip-172-31-29-45.eu-central-1.compute.internal:6667
zookeeper.connect=ip-172-31-29-45.eu-central-1.compute.internal:2181,ip-172-31-29-47.eu-central-1.compute.internal:2181,ip-172-31-29-46.eu-central-1.compute.internal:2181
```

In order to enable topic deletion, edit `/usr/hdp/current/kafka-broker/config/server.properties`
in such way:

```
$ delete.topic.enable=true
```

In ambari, this modification in transient. Every time kafka is restarted, ambari will
define a default configuration. To make such modifications persistent, you have to
edit a new kakfa configuration in ambari web service. You can add more than one kafka
broker.

To create a topic, specify the *zookeper* address. You can use node names defined in
`/etc/hosts`:

```
$ kafka-topics.sh --create --zookeeper localhost:2181 \
  --replication-factor 1 --partitions 1 --topic test
```
List all topics:

```
$ kafka-topics.sh --list --zookeeper localhost:2181
```

Create a producer. Specify *zookeper* and *listener* addresses, and topic name:

```
$ kafka-console-producer.sh --broker-list shaan-VirtualBox:9092 \
  --topic test
```

Type some text on the screen. It will reach the *consumer*. You can also `cat` a file
and stream it into kafka:

```
$ cat ~/dev/ccc-capstone/test/test.csv | \
  kafka-console-producer.sh --broker-list shaan-VirtualBox:9092 --topic test
```

In another terminal, launch
the *consumer*. Remember to specify *zookeeper* address:

```
$ kafka-console-consumer.sh --zookeeper localhost:2181 \
  --topic test --from-beginning
```

You should see all the typed text in the *producer* window. Delete a topic:

```
$ kafka-topics.sh --delete --topic test --zookeeper localhost:2181
```

Quering zookeper:

```
$ kafka-consumer-offset-checker.sh --zookeeper localhost:2181 --group spark-streaming-consumer --topic ontime
$ kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list shaan-VirtualBox:9092 --topic ontime --time -2
$ kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list shaan-VirtualBox:9092 --topic ontime --time -1
```

### Testing pyspark with kafka

You need a running *producer* since this script doesn't read a topic from beginning.
Next, you have to launch spark with the appropriate `spark-streaming-kafka-assembly`
in which your spark version appears. [here][kafka-assembly] is the address in which
libraries are. Pay attention since there is a [issue] with scala 2.11, so get the 2.10
libraries. You can get download and cache locally libraries by giving such command:

```
$ cd /home/ec2-user/capstone/streaming
$ spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 \
  kafka_wordcount.py localhost:2181 test
```

[kafka-assembly]: https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-assembly_2.10/1.5.2/
[kafka-scala-issure]: https://groups.google.com/forum/#!topic/adam-developers/j5bzgpK5-aU

### Install the Kafka Python driver

In order to create *producer* and *consumer*, you can install a python package:

```
$ yum install python-setuptools
$ easy_install pip
$ git clone https://github.com/dpkp/kafka-python.git
$ cd kafka-python
$ pip install .
$ yum install gcc-c++
$ pip install -U setuptools
$ pip install pydoop
```

## Prepare topic for exercises

Empty the `topic` and create a new topic. Then pass filtered data from HDFS with
the python `kafka-producer.py` script:

```
$ kafka-topics.sh --delete --topic ontime --zookeeper localhost:2181
$ kafka-topics.sh --create --zookeeper localhost:2181 \
  --replication-factor 1 --partitions 1 --topic ontime
$ kafka-topics.sh --list --zookeeper localhost:2181
$ cd ~/dev/ccc-capstone/ontime
$ python kafka-producer.py -d ~/dev/ccc-capstone/filtered_data/ -t ontime
```

##

Edit `/etc/security/limits.conf` as suggested [here][too-many-files-open] and [here][Too-many-open-files]

```
# To open a large number of files
*               hard    nofile          10000
```

Then edit `/usr/hdp/current/spark-client/conf/spark-env.sh` and place:

```
ulimit -n 10000
```

You have to restart all machines before using a different ulimit value.

[too-many-files-open]: http://apache-spark-user-list.1001560.n3.nabble.com/Too-many-open-files-td1464.html
[Too-many-open-files]: https://community.hortonworks.com/questions/7637/pyspark-machine-learning-get-to-many-open-file-err.html

## 1.1) Rank the top 10 most popular airports by numbers of flights to/from the airport.

Set directory to `~/dev/ccc-capstone/ontime`. Reset temporary files and topics

```
$ kafka-topics.sh --delete --topic top10_airports --zookeeper localhost:2181
$ kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 \
  --partitions 1 --topic top10_airports
$ rm -r  ~/dev/checkpoint/top10_airports/
$ rm -r  ~/dev/intermediate/top10_airports/
```

Call a *python* script:

```
$ spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 top10_airports.py
```

When there is no new output, interrupt the python script and then put the intermediate
results on new kafka topic:

```
$ python kafka-producer.py -d ~/dev/intermediate/top10_airports/ -t top10_airports --line
```

Inspect intermediate results:

```
$
$ kafka-console-consumer.sh --zookeeper localhost:2181 \
  --topic top10_airports --from-beginning
```

Then call the final script:

```
$ rm -r  ~/dev/checkpoint/top10_airports.2/
$ rm -r  ~/dev/final/top10_airports/
$ spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 \
  --master yarn --executor-cores=3 --num-executors 4 --driver-memory=3G --executor-memory=6G \
  top10_airports.2.py
```

Here's the top10 airport

```
(ORD,12449354)
(ATL,11540422)
(DFW,10799303)
(LAX,7723596)
(PHX,6585532)
(DEN,6273787)
(DTW,5636622)
(IAH,5480734)
(MSP,5199213)
(SFO,5171023)
```

## 1.2) Rank the top 10 airlines by on-time arrival performance.

Set directory to `~/dev/ccc-capstone/ontime`. Reset temporary files and topics

```
$ kafka-topics.sh --delete --topic top10_airlines --zookeeper localhost:2181
$ kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 \
  --partitions 1 --topic top10_airlines
$ rm -r  ~/dev/checkpoint/top10_airlines/
$ rm -r  ~/dev/intermediate/top10_airlines/
```

Call a *python* script:

```
cd ~/dev/aws_spark/spark
$ spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 airport_1.2.py
  --master yarn --executor-cores=3 --num-executors 4 --driver-memory=3G --executor-memory=6G 
```

When there is no new output, interrupt the python script and then put the intermediate
results on new kafka topic:

```
$ python kafka-producer.py -d /user/paolo/intermediate/top10_airlines/ -t top10_airlines
```

Then call the final script:

```
$ spark-submit --packages org.apache.spark:spark-streaming-kafka-assembly_2.10:1.3.1 \
  --master yarn --executor-cores=3 --num-executors 4 --driver-memory=3G --executor-memory=6G \
  top10_airlines.2.py
```

Here's the top10 airlines:

```
(19690, -1.01180434574519)                                                      
(19678, 1.1569234424812056)
(19391, 1.4506385127822803)
(20295, 4.747609195734892)
(20384, 5.3224309999287875)
(20436, 5.465881148819851)
(19386, 5.557783392671835)
(19393, 5.5607742598815735)
(20304, 5.736312463662878)
(20363, 5.8671846616957595)
```
