#!/usr/bin/python

#

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='152.46.17.34')

producer.send('test', b'chirag vijay')
