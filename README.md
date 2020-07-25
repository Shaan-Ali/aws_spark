# aws_spark

1a. 
sudo yum install git
git --version
git clone https://github.com/Shaan-Ali/aws_spark.git

1b. 
sudo -i
pip install pykafka
sudo yum install java-1.8.0
spark-submit --version
exit

2. 
chmod 777 ./aws_spark/kafka_setup.sh
./aws_spark/kafka_setup.sh

3. New:
./kafka/bin/zookeeper-server-start.sh ./kafka/config/zookeeper.properties

4. New:
./kafka/bin/kafka-server-start.sh ./kafka/config/server.properties

5a. New: 
export PATH=$PATH:/home/hadoop/kafka/bin/
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic order_data
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic orders_ten_sec_data


5b. Push Topic
chmod 777 ./aws_spark/run_push_data.sh
./aws_spark/run_push_data.sh ip-172-31-63-86

6. Start spark job 
spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 ./aws_spark/spark/spark_streaming_airport.py localhost:2181 order_data

=======
others: for help:
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

./spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0  --jars spark-streaming-kafka-assembly_2.10-1.6.0.jar spark_streaming_order_status.py localhost:2181 order_data