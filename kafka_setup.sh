wget http://archive.apache.org/dist/kafka/0.11.0.0/kafka_2.11-0.11.0.0.tgz
tar -xzf kafka_2.11-0.11.0.0.tgz
mv kafka_2.11-0.11.0.0 kafka
cd kafka

export PATH=$PATH:/home/hadoop/kafka/bin/
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic order_data
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic orders_ten_sec_data
