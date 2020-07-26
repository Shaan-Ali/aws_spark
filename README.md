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
chmod 777 ./aws_spark/run_spark.sh

2. Kafka Setup:
./aws_spark/kafka_setup.sh

** Start **
3. New:
./kafka/bin/zookeeper-server-start.sh ./kafka/config/zookeeper.properties

4. New:
./kafka/bin/kafka-server-start.sh ./kafka/config/server.properties


5. Push Topic
/bin/bash ./aws_spark/kafka/push_data_in_topic.sh ./aws_spark/data $BrL AWSKafkaTutorialTopic

6. Start spark job 
spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 --master yarn --executor-cores=4 --num-executors 16 --driver-memory=4G --executor-memory=12G 
./aws_spark/spark/spark_streaming_airport.py localhost:2181 AWSKafkaTutorialTopic
 

=======
others: for help:
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

./spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0  --jars spark-streaming-kafka-assembly_2.10-1.6.0.jar spark_streaming_order_status.py localhost:2181 order_data

./kafka-console-producer.sh --broker-list b-2.awskafkatutorialcluste.pbiu94.c1.kafka.us-east-1.amazonaws.com:9094,b-1.awskafkatutorialcluste.pbiu94.c1.kafka.us-east-1.amazonaws.com:9094,b-3.awskafkatutorialcluste.pbiu94.c1.kafka.us-east-1.amazonaws.com:9094 --producer.config client.properties --topic AWSKafkaTutorialTopic

./kafka-console-consumer.sh --bootstrap-server b-2.awskafkatutorialcluste.pbiu94.c1.kafka.us-east-1.amazonaws.com:9094,b-1.awskafkatutorialcluste.pbiu94.c1.kafka.us-east-1.amazonaws.com:9094,b-3.awskafkatutorialcluste.pbiu94.c1.kafka.us-east-1.amazonaws.com:9094 --consumer.config client.properties --topic AWSKafkaTutorialTopic --from-beginning