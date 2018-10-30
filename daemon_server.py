#!/usr/bin/python

import argparse
import multiprocessing
import time

from kafka import KafkaProducer

server_count = 100
server_start = 0

def worker_node():
    '''
    The simulation of a single server
    '''
    producer = KafkaProducer(bootstrap_servers='152.46.16.59')
    while True:
        try:
            print("Hello" + multiprocessing.current_process().name)
            producer.send('test', "Hello" + multiprocessing.current_process().name)
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
