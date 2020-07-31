# Running in Ubuntu
# In all new window:
cd dev

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

export JRE_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre

export SPARK_HOME=/usr/local/spark

export PATH=$PATH:/home/shaan/dev/kafka/bin/

export PATH=$PATH:$SPARK_HOME/bin/

echo $PATH

====================================
#1. New:
zookeeper-server-start.sh ./kafka/config/zookeeper.properties

#2. New:
kafka-server-start.sh ./kafka/config/server.properties

#3a. New: 
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic order_data

#3b. Data start:
cd ~/dev/aws_spark/kafka

/bin/bash ./push_data_in_topic.sh ../data shaan-VirtualBox:9092 order_data

#4. New: Spark start: 
cd ~/dev/aws_spark/spark

spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0  airport_1.3.py


#==========================================
==========================================
# One time setup
1a. 
sudo -i
yum install git
pip install pykafka
sudo yum install java-1.8.0
exit
git --version
spark-submit --version

1b.
git clone https://github.com/Shaan-Ali/aws_spark.git
chmod 777 ./aws_spark/kafka_setup.sh
chmod 777 ./aws_spark/run_spark.sh

2. Kafka Setup:
./aws_spark/kafka_setup.sh
==================
# Others: for help:
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
./spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0  --jars spark-streaming-kafka-assembly_2.10-1.6.0.jar spark_streaming_order_status.py localhost:2181 order_data

--master yarn --executor-cores=4 --num-executors 16 --driver-memory=4G --executor-memory=12G
 localhost:2181 AWSKafkaTutorialTopic
$SPARK_HOME/bin/pyspark


spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 --master yarn --executor-cores=4 --num-executors 16 --driver-memory=4G --executor-memory=12G 
./aws_spark/spark/spark_streaming_airport.py localhost:2181 AWSKafkaTutorialTopic

-- kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic orders_ten_sec_data

$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 ./aws_spark/spark/spark_streaming_airport.py localhost:2181 order_data
$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 spark_ubuntu.py localhost:2181 airport_data

/bin/bash ./aws_spark/kafka/push_data_in_topic.sh ./aws_spark/data shaan-VirtualBox:9092 order_data
./kafka/bin/kafka-console-producer.sh --broker-list shaan-VirtualBox92  --topic order_data