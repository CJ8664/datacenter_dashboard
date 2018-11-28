#!/usr/bin/python

import argparse
import multiprocessing
import time
from kafka import KafkaProducer
import random
import time
import json

from datetime import datetime

server_count = 100
server_start = 0

kafka_ips = ['35.211.13.141', '35.211.21.153', '35.211.37.39']

class Metric:
    def __init__(self, name, range_low, range_high):
        self.name = name
        self.low = range_low
        self.high = range_high

    def __repr__(self):
        return "({}:{})".format(self.low, self.high)


def generate_metric():
    '''
    Actual data, seperated by ,
    '''

    metrics = [
        Metric("cpu_usage", 0, 100),
        Metric("memory_utilization", 0, 100),
        Metric("temperature", -100, 100),
        Metric("disk_usage", 100, 500),
        Metric("io_usage", -200, -100)
    ]

    server_id = multiprocessing.current_process().name
    endoded_data = encode_as_json(server_id, metrics)
    return endoded_data

def encode_as_json(server_id, metrics):

    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    packet = {}
    packet['server_id'] = server_id
    packet['time'] = timestamp
    packet['server_time'] = timestamp

    for m in metrics:
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
            producer.send('test4', json_data)
            # print(multiprocessing.current_process().name + " sent")
            time.sleep(1)
        except KeyboardInterrupt as ex:
            break
        except Exception as exp:
            print(exp)


def create_server_farm():
    '''
    The function responsible to start threads that will simulate the servers
    '''

    servers = [ multiprocessing.Process(name='server_{}'.format(server_start + num), target=worker_node) for num in range(server_count)]
    for server in servers:
        server.start()
    for server in servers:
        server.join()


def main():
    '''
    Start point of the program and master of all child threaads
    '''
    global server_count, server_start, kill_switch

    parser = argparse.ArgumentParser(description='This program generates synthetic data for the Kafka Stream simulating the Server Farm')
    parser.add_argument('-c', action='store', dest='server_count', help='Server count', required=True, type=int)
    parser.add_argument('-s', action='store', dest='server_start', help='Server count', required=True, type=int)

    args = parser.parse_args()

    server_count = args.server_count
    server_start = args.server_start

    try:
        create_server_farm()
    except KeyboardInterrupt as ex:
        print('\nStopping Server Farm')


if __name__ == '__main__':
    main()
