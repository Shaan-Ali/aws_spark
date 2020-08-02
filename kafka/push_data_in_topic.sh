#!/bin/bash

export PATH=$PATH:/home/hadoop/kafka/bin
FILES=$1/*.csv

for f in $FILES
do
    echo "pushing $f file"
#    cat $f | kafka-console-producer.sh --broker-list $2  --producer.config /home/hadoop/kafka/bin/client.properties --topic $3
    cat $f | kafka-console-producer.sh --broker-list $2  --topic $3
#    sleep 10
done

#./kafka-console-producer.sh --broker-list
#    b-2.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094,b-3.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094,b-1.awskafkatutorialcluste.ea4k5h.c1.kafka.us-east-1.amazonaws.com:9094
#    --producer.config client.properties --topic order_data