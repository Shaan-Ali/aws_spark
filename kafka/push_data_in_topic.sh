#!/bin/bash

FILES=$1/*.csv

for f in $FILES
do
    echo "pushing $f file"
    cat $f | kafka-console-producer.sh --broker-list $2  --producer.config client.properties  --topic $3
    sleep 60
done

#export PATH=$PATH:/home/hadoop/kafka/bin
