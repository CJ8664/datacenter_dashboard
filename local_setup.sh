#!/bin/zsh

export ANSIBLE_HOST_KEY_CHECKING="False"

echo stat | nc 35.185.126.8 2181 | grep -i mode
echo stat | nc 35.237.132.111 2181 | grep -i mode
echo stat | nc 35.243.248.64 2181 | grep -i mode


echo stat | nc 35.211.13.141 9092
echo stat | nc 35.211.21.153 9092
echo stat | nc 35.211.37.39 9092
echo stat | nc 35.211.83.103 9092
echo stat | nc 35.211.51.202 9092
echo stat | nc 35.211.149.62 9092


echo dump | nc 35.237.132.111 2181 | grep brokers

./kafka-topics.sh --create --zookeeper 35.185.126.8:2181 --replication-factor 6 --partitions 1 --topic logs-topic
./kafka-topics.sh --create --zookeeper 35.185.126.8:2181 --replication-factor 6 --partitions 1 --topic metrics-topic
./kafka-topics.sh --create --zookeeper 35.185.126.8:2181 --replication-factor 6 --partitions 1 --topic datacenter-metrics

curl -X POST -H 'Content-Type: application/json' -d @log_spec.json http://35.231.108.142:8090/druid/indexer/v1/supervisor
curl -X POST -H 'Content-Type: application/json' -d @metrics_spec.json http://35.231.108.142:8090/druid/indexer/v1/supervisor
