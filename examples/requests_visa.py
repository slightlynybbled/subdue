import json

import requests
import time
from datetime import datetime


def post_to_device(sn, command):
    host = 'http://localhost:5001/visa/{}'.format(sn)

    start_time = datetime.now()
    response = requests.post(host, json=command)
    end_time = datetime.now()

    print('request: ', command)
    print('response (json): ', response.json())
    print('headers:', response.headers)
    print('timedelta', end_time - start_time)
    print()

"""
find all attached devices
"""
r = requests.post('http://localhost:5001/attached')
attached = r.json()
sn = attached['visa'][0]['SerialNumber']    # assumes only one PSU is attached
print('attached: ', attached)
print('sn: ', sn)

# power supply control commands
post_to_device(sn, {'operation': 'write', 'parameter': 'voltage', 'value': 2.0})    # write to PSU voltage
post_to_device(sn, {'operation': 'write', 'parameter': 'current', 'value': 2.0})    # write to PSU current

post_to_device(sn, {'operation': 'write', 'parameter': 'ocp', 'value': True})       # psu OCP on
post_to_device(sn, {'operation': 'write', 'parameter': 'output', 'value': True})    # psu on/off

time.sleep(0.5)  # wait for output to stabilize before attempting a read

post_to_device(sn, {'operation': 'read', 'parameter': 'voltage'})   # read voltage
post_to_device(sn, {'operation': 'read', 'parameter': 'current'})   # read current
post_to_device(sn, {'operation': 'read', 'parameter': 'status'})   # read status

post_to_device(sn, {'operation': 'reset'})   # reset
