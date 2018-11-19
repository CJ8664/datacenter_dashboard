#!/usr/bin/python

import argparse
import multiprocessing
import time
from kafka import KafkaProducer
import random

server_count = 100
server_start = 0

kafka_ips = ['35.211.13.141', '35.211.21.153', '35.211.37.39']

class Metric:
    def __init__(self, range_low, range_high):
        self.low = range_low
        self.high = range_high

    def __repr__(self):
        return "({}:{})".format(self.low, self.high)


def generate_metric():
    '''
    Actual data, seperated by ,
    '''

    metrics = [
        Metric(0, 10),
        Metric(0, 100),
        Metric(-100, 100),
        Metric(100, 500),
        Metric(-200, -100)
    ]

    print(metrics)
    data = [random.randint(m.low, m.high) for m in metrics]
    endoded_data = ','.join(str(v) for v in data)
    server_id = multiprocessing.current_process().name

    return "{}:{}".format(server_id, endoded_data)


def worker_node():
    '''
    The simulation of a single server
    '''

    # ./kafka-topics.sh --create --zookeeper 184.73.102.168:2181,52.5.27.230:2181,54.159.237.81:2181 --replication-factor 3 --partitions 1 --topic test
    # ./kafka-topics.sh --list --zookeeper 184.73.102.168:2181
    producer = KafkaProducer(bootstrap_servers=kafka_ips, api_version=(2, 0, 0))
    
    while True:
        try:
            # print("Hello" + multiprocessing.current_process().name)
            # producer.send('test', "Hello" + multiprocessing.current_process().name)
            data = generate_metric()
            print(data)
            producer.send('test', str.encode(data))
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
