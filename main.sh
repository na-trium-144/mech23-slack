#!/bin/sh
cd `dirname $0`
pip install -r requirements.txt

python3 ./app.py &

while true; do python3 ./mech_office.py; sleep 21600; done &
while true; do python3 ./mech_a_internal.py; sleep 21600; done &
# while true; do python3 ./gcal-to-slack.py; sleep 86400; done &

wait
