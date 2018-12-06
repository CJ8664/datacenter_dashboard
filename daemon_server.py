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
from numpy import random

server_count = 100
server_start = 1
datacenter_count = 5
datacenter_start = 1

topic_name = 'datacenter-metrics'

kafka_ips = ['35.211.13.141', '35.211.21.153', '35.211.37.39']
log_levels = ['INFO','DEBUG','WARN','ERROR','CRITICAL']
log_texts = ['Connected to Database', 'Order confirmation saved', 'Unable to find product', 'Trasaction failed ID#2343213']

class Metric:
    def __init__(self, name, mean, stddev):
        self.name = name
        self.mean = mean
        self.stddev = stddev

    def __repr__(self):
        return "({}:{})".format(self.mean, self.stddev)


def generate_metric():
    '''
    Actual data in dictionary
    '''

    metrics = [
        Metric("cpu_usage", 60, 5),
        Metric("memory_usage", 50, 10),
        Metric("temperature", 60, 2),
        Metric("disk_usage", 55, 3),
        Metric("io_usage", 50, 20),
        Metric("heartbeat", 0, 2),
        Metric("log_level", 0, 5),
        Metric("log_text", 0, 4)
    ]

    process_name = multiprocessing.current_process().name.split('#')
    datacenter_id = process_name[0]
    server_id = process_name[1]

    endoded_data = encode_as_json(datacenter_id, server_id, metrics)

    return endoded_data

def encode_as_json(datacenter_id, server_id, metrics):

    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    packet = OrderedDict()
    packet['server_id'] = server_id
    packet['datacenter_id'] = datacenter_id
    packet['server_time'] = timestamp

    for m in metrics:
        if (m.name == "log_level"):
            packet[m.name] = log_levels[random.randint(m.mean, m.stddev)]
        elif (m.name == "heartbeat"):
            # Need randomization
            packet[m.name] = random.randint(m.mean, m.stddev)
        elif (m.name == "log_text"):
            packet[m.name] = log_texts[random.randint(m.mean, m.stddev)]
        else:
            packet[m.name] = get_normal_random(m.mean, m.stddev)

    json_data = json.dumps(packet)
    return json_data

def get_normal_random(mu, var):
    '''
    Helper method to generate random number
    given the mean and standard deviation=1
    '''
    return int(random.normal(mu, var, 1))


def worker_node():
    '''
    The simulation of a single server
    '''
    producer = KafkaProducer(bootstrap_servers=kafka_ips)

    while True:
        try:
            json_data = generate_metric()
            # print(json_data)
            producer.send(topic_name, json_data)
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
            servers.append(multiprocessing.Process(name='datacenter_{}#server_{}'.format(datacenter_idx + datacenter_start , server_idx + server_start), target=worker_node))

    print("Started sending data")
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
