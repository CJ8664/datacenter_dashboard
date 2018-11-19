#!/bin/sh
sudo apt-get update && sudo apt-get install software-properties-common

#Step 2: Add the Ansible repository to your system
sudo apt-add-repository ppa:ansible/ansible

#Step 3: Install Ansible
sudo apt-get update && sudo apt-get install ansible
