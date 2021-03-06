Intro - Chirag 2 mins
Show The realtime Dashbord
Talk about Architecture
  Not standalone, cluster, distributed,
  not running on docker or localhost, single machine setup
  Not managed services, static IPs
  - Zookeeper running on independent node and not on Druid/Kafka
  - Two server with python daemon
  - Sample data {"server_id": "server_37", "datacenter_id": "datacenter_2", "time": "2018-12-05T22:22:39", "cpu_usage": 58, "memory_usage": 52, "temperature": 56, "disk_usage": 53, "io_usage": 52, "heartbeat": 0, "log_level": "WARN", "log_text": "asdasdasd"}
  - Kafka Brokers
  - Java stream API, split data
  - Ingested by Druid worker
  - Visible on superset

First origin of data is in python daemon running on
Google Server and simulates data for 500 server. We have used normal distribution
to mimic an actual server

Now this data is sent to Kafka datacenter-metrics (show on console)

Now Kafka streaming api pulls this raw feed and processes the stream in realtime
to split data in metrics and log (show on console). Sends back on kafka topics

Since push/pull we have Druid injection service to consume the data from Kafka and store it
in segments following the Lamda Architecture

Superset is the Analytics tool, it queries the data in realtime from Druid
Explain charts.


Scenarios
- Add load (run python on new google server)
- Kill the leader, new leader is elected, Bring back the dead, no change leader
- Kill Injestion service

nohup python daemon_server.py --server-count 100 --server-start 1 --datacenter-count 5 --datacenter-start 1 &
nohup python daemon_server.py --server-count 100 --server-start 1 --datacenter-count 25 --datacenter-start 6 &

Sample data {"server_id": "server_37", "datacenter_id": "datacenter_2", "time": "2018-12-05T22:22:39", "cpu_usage": 58, "memory_usage": 52, "temperature": 56, "disk_usage": 53, "io_usage": 52, "heartbeat": 0, "log_level": "WARN", "log_text": "asdasdasd"}

./kafka-console-consumer.sh --bootstrap-server 35.211.13.141:9092 --topic datacenter-metrics
./kafka-console-consumer.sh --bootstrap-server 35.211.13.141:9092 --topic logs-topic
./kafka-console-consumer.sh --bootstrap-server 35.211.13.141:9092 --topic metrics-topic

echo stat | nc 35.185.126.8 2181 | grep -i mode
echo stat | nc 35.237.132.111 2181 | grep -i mode
echo stat | nc 35.243.248.64 2181 | grep -i mode

ansible-playbook -i inventory.yml playbooks/leader_kill.yml
ansible-playbook -i inventory.yml playbooks/leader_start.yml

echo stat | nc 35.185.126.8 2181 | grep -i mode
echo stat | nc 35.237.132.111 2181 | grep -i mode
echo stat | nc 35.243.248.64 2181 | grep -i mode

ansible-playbook -i inventory.yml playbooks/ksh_kill.yml
ansible-playbook -i inventory.yml playbooks/ksh_start.yml

curl -X POST -H 'Content-Type: application/json' -d @log_spec.json http://35.231.108.142:8090/druid/indexer/v1/supervisor
curl -X POST -H 'Content-Type: application/json' -d @metrics_spec.json http://35.231.108.142:8090/druid/indexer/v1/supervisor
