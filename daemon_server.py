#!/usr/bin/python

import argparse
import multiprocessing
import time
from kafka import KafkaProducer
import random
import time
import json

from collections import OrderedDict
from datetime import datetime

server_count = 100
server_start = 1
datacenter_count = 5
datacenter_start = 1

kafka_ips = ['35.211.13.141', '35.211.21.153', '35.211.37.39']
log_levels = ['INFO','DEBUG','WARN','ERROR','CRITICAL']
log_texts = ['asdasdasd', 'adafvweewe']

class Metric:
    def __init__(self, name, range_low, range_high):
        self.name = name
        self.low = range_low
        self.high = range_high

    def __repr__(self):
        return "({}:{})".format(self.low, self.high)


def generate_metric():
    '''
    Actual data in dictionary
    '''

    metrics = [
        Metric("cpu_usage", 0, 100),
        Metric("memory_usage", 0, 100),
        Metric("temperature", 0, 100),
        Metric("disk_usage", 100, 500),
        Metric("io_usage", 0, 100),
        Metric("heartbeat", 0, 1),
        Metric("log_level", 0, 4),
        Metric("log_text", 0, 1)
    ]

    process_name = multiprocessing.current_process().name.split('#')
    data_center_id = process_name[0]
    server_id = process_name[1]

    endoded_data = encode_as_json(data_center_id, server_id, metrics)

    return endoded_data

def encode_as_json(data_center_id, server_id, metrics):

    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    packet = OrderedDict()
    packet['server_id'] = server_id
    packet['data_center_id'] = data_center_id
    packet['time'] = timestamp

    for m in metrics:
        if (m.name == "log_level"):
            packet[m.name] = log_levels[random.randint(m.low, m.high)]
        elif (m.name == "heartbeat"):
            # Need randomization
            packet[m.name] = random.randint(m.low, m.high)
        elif (m.name == "log_text"):
            packet[m.name] = log_texts[random.randint(m.low, m.high)]
        else:
            packet[m.name] = random.randint(m.low, m.high)

    json_data = json.dumps(packet, encoding="utf-8")
    return json_data


def worker_node():
    '''
    The simulation of a single server
    '''
    # ./kafka-console-producer.sh --broker-list 35.211.13.141:9092 --topic test
    # ./kafka-console-consumer.sh --bootstrap-server 35.211.13.141:9092 --topic test --from-beginning
    # ./kafka-topics.sh --create --zookeeper 184.73.102.168:2181,52.5.27.230:2181,54.159.237.81:2181 --replication-factor 1 --partitions 1 --topic test
    # ./kafka-topics.sh --create --zookeeper 184.73.102.168:2181,52.5.27.230:2181,54.159.237.81:2181 --replication-factor 3 --partitions 1 --topic test
    # ./kafka-topics.sh --list --zookeeper 184.73.102.168:2181
    # ./kafka-topics.sh --delete --zookeeper 184.73.102.168:2181 --topic test
    producer = KafkaProducer(bootstrap_servers=kafka_ips)

    while True:
        try:
            json_data = generate_metric()
            print(json_data)
            producer.send('datacenter_metrics', json_data)
            # print(multiprocessing.current_process().name + " sent")
            time.sleep(1)
        except KeyboardInterrupt as ex:
            break
        except Exception as exp:
            print(exp)


def create_datacenters():
    '''
    The function responsible to start threads that will simulate the servers
    '''

    servers = []
    for datacenter_idx in range(datacenter_count):
        for server_idx in range(server_count):
            servers.append(multiprocessing.Process(name='data_center_{}#server_{}'.format(datacenter_idx + datacenter_start , server_idx + server_start), target=worker_node))

    for server in servers:
        server.start()
    for server in servers:
        server.join()


def main():
    '''
    Start point of the program and master of all child threaads
    '''
    global server_count, server_start, datacenter_count, datacenter_start, kill_switch

    parser = argparse.ArgumentParser(description='This program generates synthetic data for the Kafka Stream simulating the Server Farm')
    parser.add_argument('--server-count', action='store', dest='server_count', help='Server count', required=True, type=int)
    parser.add_argument('--server-start', action='store', dest='server_start', help='Server start index', required=True, type=int)
    parser.add_argument('--datacenter-count', action='store', dest='datacenter_count', help='Datacenter count', required=True, type=int)
    parser.add_argument('--datacenter-start', action='store', dest='datacenter_start', help='Datacenter start index', required=True, type=int)

    args = parser.parse_args()

    server_count = args.server_count
    server_start = args.server_start

    datacenter_count = args.datacenter_count
    datacenter_start = args.datacenter_start

    try:
        create_datacenters()
    except KeyboardInterrupt as ex:
        print('\nStopping datacenters')


if __name__ == '__main__':
    main()
