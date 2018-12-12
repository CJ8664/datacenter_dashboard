import subprocess
import sys
import time

from subprocess import call

def create_inv(ip_id_list):
    user = "ansible_user=csjain"
    key = "ansible_ssh_private_key_file=/Users/chiragjain/.ssh/id_gcp"
    with open('temp_inventory.yml', 'w') as fh:
        fh.write("[kafka]\n")
        for ip, id in ip_id_list:
            fh.write("{} kafka_brokerid={} {} {}\n".format(ip, id, user, key))

    call(["ansible-playbook", "-i", "temp_inventory.yml", "playbooks/kafka_stop_start.yml"])
    print("Broker started")
    time.sleep(20)

broker_set = ['/brokers/ids/1', '/brokers/ids/2', '/brokers/ids/3', '/brokers/ids/4', '/brokers/ids/5', '/brokers/ids/6']

while True:
    brokers = subprocess.Popen("echo dump | nc 35.237.132.111 2181 | grep brokers", shell=True, stdout=subprocess.PIPE).stdout.read().strip()
    up_brokers = [x.strip() for x in brokers.split("\n")]
    down_brokers = []
    print("Checking all broker are up")
    for broker in broker_set:

        if broker not in up_brokers:
            print(broker + " is down, brining it up")
            if broker == "/brokers/ids/1":
                down_brokers.append(("35.211.13.141", 1))
            elif broker == "/brokers/ids/2":
                down_brokers.append(("35.211.21.153", 2))
            elif broker == "/brokers/ids/3":
                down_brokers.append(("35.211.37.39", 3))
            elif broker == "/brokers/ids/4":
                down_brokers.append(("35.211.83.103", 4))
            elif broker == "/brokers/ids/5":
                down_brokers.append(("35.211.51.202", 5))
            elif broker == "/brokers/ids/6":
                down_brokers.append(("35.211.149.62", 6))

    if len(down_brokers) > 0:
        create_inv(down_brokers)
        
    time.sleep(10)
