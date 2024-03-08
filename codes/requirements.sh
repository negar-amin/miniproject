#!/bin/sh
apt-get update
apt-get upgrade
apt-get install cron
apt-get install nano
export EDITOR=nano
apt-get install python3
apt-get install python3-pip
pip3 install kafka-python
pip3 install requests
pip3 install psycopg2-binary
pip3 install faker
chmod +x script.sh
