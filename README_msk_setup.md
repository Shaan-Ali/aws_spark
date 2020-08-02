sg-05f27161669d5073b

================================================
sudo yum install java-1.8.0
wget https://archive.apache.org/dist/kafka/2.2.1/kafka_2.12-2.2.1.tgz
tar -xzf kafka_2.12-2.2.1.tgz
mv kafka_2.12-2.2.1 kafka
rm kafka_2.12-2.2.1.tgz
cd kafka

================================================
	aws kafka describe-cluster --region us-east-1 --cluster-arn "arn:aws:kafka:us-east-1:336162387709:cluster/AWSKafkaTutorialCluster/b4a2fc66-03c8-47f6-bd83-f0030145bf3f-1"
	bin/kafka-topics.sh --create --zookeeper ZookeeperConnectString --replication-factor 3 --partitions 1 --topic order_data
	bin/kafka-topics.sh --create --zookeeper z-1.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:2181,z-2.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:2181,z-3.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:2181 --replication-factor 3 --partitions 1 --topic order_data

ls /usr/lib/jvm/
cp /usr/lib/jvm/java-1.8.0-amazon-corretto.x86_64/jre/lib/security/cacerts /tmp/kafka.client.truststore.jks

cd kafka/bin
vi client.properties
security.protocol=SSL
ssl.truststore.location=/tmp/kafka.client.truststore.jks


aws kafka get-bootstrap-brokers --region us-east-1 --cluster-arn arn:aws:kafka:us-east-1:336162387709:cluster/AWSKafkaTutorialCluster/b4a2fc66-03c8-47f6-bd83-f0030145bf3f-1
./kafka-console-producer.sh --broker-list <BootstrapBrokerStringTls> --producer.config client.properties --topic order_data
./kafka-console-producer.sh --broker-list 
    b-2.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094,b-3.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094,b-1.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094 
    --producer.config client.properties --topic order_data

#Main setting:
kafka-console-consumer.sh --bootstrap-server b-2.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094,b-3.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094,b-1.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094  --topic order_data --from-beginning

=================
sg-04b26dcd3337d9765
AwsSubnet-2

vpc-05b171cc72b7e8cb6		sg-0357f01d9e220332b
arn:aws:kafka:us-east-1:336162387709:cluster/AWSKafkaTutorialCluster/b4a2fc66-03c8-47f6-bd83-f0030145bf3f-1


aws kafka describe-cluster --region us-east-1 --cluster-arn "arn:aws:kafka:us-east-1:336162387709:cluster/AWSKafkaTutorialCluster/b4a2fc66-03c8-47f6-bd83-f0030145bf3f-1"
===============