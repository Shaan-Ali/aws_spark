# CCC - Task 2

# Data:
mkdir data 

aws s3 cp s3://aws-bucket-0730/ data  --recursive

# Setup: 
sudo -i

yum install git

pip install pykafka

sudo yum install java-1.8.0

exit

git --version

spark-submit --version

# Git & Kafka:

git clone https://github.com/Shaan-Ali/aws_spark.git

chmod 744 ./aws_spark/kafka_setup.sh

chmod 744 ./aws_spark/run_spark.sh

./aws_spark/kafka_setup.sh

export PATH=$PATH:/home/hadoop/kafka/bin/


# ** Start **
#1. Zk start: 
./kafka/bin/zookeeper-server-start.sh ./kafka/config/zookeeper.properties

#2. New: Kafka start
./kafka/bin/kafka-server-start.sh ./kafka/config/server.properties

#3. New: Push Topic & Data
export PATH=$PATH:/home/hadoop/kafka/bin/

kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic order_data

cd ./aws_spark/kafka/

/bin/bash ./push_data_in_topic.sh ../data ip-172-31-41-74:9092 order_data

/bin/bash ./push_data_in_topic.sh ../data/     b-2.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094,b-3.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094,b-1.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094   order_data
---
kafka-topics.sh --delete --topic order_date --zookeeper master:2181
kafka-topics.sh --list --zookeeper master:2181


#4. New: Start spark job 
kafka-console-consumer.sh --bootstrap-server b-2.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094,b-3.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094,b-1.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094 --consumer.config /home/hadoop/kafka/bin/client.properties \
--topic order_data --from-beginning


cd ~/aws_spark/spark/
spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0  airport_1.3.py

spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 --master yarn --executor-cores=4 --num-executors 16 --driver-memory=4G --executor-memory=12G 
           airport_1.3.py localhost:2181
#=================================================
# others: for help:
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

./spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0  --jars spark-streaming-kafka-assembly_2.10-1.6.0.jar spark_streaming_order_status.py localhost:2181 order_data

./kafka-console-producer.sh --broker-list b-2.awskafkatutorialcluste.pbiu94.c1.kafka.us-east-1.amazonaws.com:9094,b-1.awskafkatutorialcluste.pbiu94.c1.kafka.us-east-1.amazonaws.com:9094,b-3.awskafkatutorialcluste.pbiu94.c1.kafka.us-east-1.amazonaws.com:9094 --producer.config client.properties --topic AWSKafkaTutorialTopic

./kafka-console-consumer.sh --bootstrap-server b-2.awskafkatutorialcluste.pbiu94.c1.kafka.us-east-1.amazonaws.com:9094,b-1.awskafkatutorialcluste.pbiu94.c1.kafka.us-east-1.amazonaws.com:9094,b-3.awskafkatutorialcluste.pbiu94.c1.kafka.us-east-1.amazonaws.com:9094 --consumer.config client.properties --topic AWSKafkaTutorialTopic --from-beginning

    /bin/bash ./aws_spark/kafka/push_data_in_topic.sh ./aws_spark/data ip-172-31-59-7:9092 order_data
--- /bin/bash ./aws_spark/kafka/push_data_in_topic.sh ./aws_spark/data shaan-VirtualBox:9092 order_data
-- spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 --master yarn --executor-cores=4 --num-executors 16 --driver-memory=4G --executor-memory=12G 
           ./aws_spark/spark/spark_streaming_airport.py localhost:2181 AWSKafkaTutorialTopic
           
export KAFKA_HEAP_OPTS="-Xmx250M -Xms250M"


