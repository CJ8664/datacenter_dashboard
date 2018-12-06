#!/bin/zsh

export ANSIBLE_HOST_KEY_CHECKING="False"

echo stat | nc 35.185.126.8 2181 | grep -i mode
echo stat | nc 35.237.132.111 2181 | grep -i mode
echo stat | nc 35.243.248.64 2181 | grep -i mode

./kafka-topics.sh --create --zookeeper 35.185.126.8:2181 --replication-factor 1 --partitions 1 --topic logs-topic
./kafka-topics.sh --create --zookeeper 35.185.126.8:2181 --replication-factor 1 --partitions 1 --topic metrics-topic
./kafka-topics.sh --create --zookeeper 35.185.126.8:2181 --replication-factor 1 --partitions 1 --topic datacenter-metrics

#
# curl -X POST -H 'Content-Type: application/json' -d @log_spec.json http://35.231.108.142:8090/druid/indexer/v1/supervisor
# curl -X POST -H 'Content-Type: application/json' -d @metrics_spec.json http://35.231.108.142:8090/druid/indexer/v1/supervisor
