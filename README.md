# aws_spark
wget http://archive.apache.org/dist/kafka/0.11.0.0/kafka_2.11-0.11.0.0.tgz
tar -xzf kafka_2.11-0.11.0.0.tgz
mv kafka_2.11-0.11.0.0 kafka
cd kafka

export PATH=$PATH:/home/hadoop/kafka/bin/
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic order_data
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic orders_ten_sec_data


./bin/zookeeper-server-start.sh config/zookeeper.properties
./bin/kafka-server-start.sh config/server.properties
====
sudo yum install git
git --version
git clone https://github.com/raghushining/spark-project.git

sudo -i
pip install pykafka

sudo yum install java-1.8.0
spark-submit --version
====
cd /home/hadoop/spark-project/spark_dashboard/kafka
/bin/bash push_orders_data_in_topic.sh ../data/ordersdata/ ip-172-31-44-36:9092 order_data

cd /home/hadoop/spark-project/spark_dashboard/spark
spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 spark_streaming_order_status.py localhost:2181 order_data
===
others: for help:
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

./spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0  --jars spark-streaming-kafka-assembly_2.10-1.6.0.jar spark_streaming_order_status.py localhost:2181 order_data