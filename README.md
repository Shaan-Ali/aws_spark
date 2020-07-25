# aws_spark

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
chmod 777 ./aws_spark/run_push_data.sh
chmod 777 ./aws_spark/run_spark.sh

2. Kafka Setup:
./aws_spark/kafka_setup.sh

** Start **
3. New:
./kafka/bin/zookeeper-server-start.sh ./kafka/config/zookeeper.properties

4. New:
./kafka/bin/kafka-server-start.sh ./kafka/config/server.properties

5a. New: 
export PATH=$PATH:/home/hadoop/kafka/bin/
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic order_data
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic orders_ten_sec_data


5b. Push Topic
./aws_spark/run_push_data.sh ip-172-31-63-86                /update Ip

6. Start spark job 
cd aws_spark
./run_spark.sh

=======
others: for help:
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

./spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0  --jars spark-streaming-kafka-assembly_2.10-1.6.0.jar spark_streaming_order_status.py localhost:2181 order_data