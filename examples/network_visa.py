import time
import requests

r = requests.post('http://localhost:5001/attached')
print('attached: ', r.json())

# get the first PSU attached
device_reference = r.json()['visa'][0]  # assumes only one PSU is attached
url = 'http://localhost:5001/visa/{}'.format(device_reference)

# power supply control commands
data = {'operation': 'write', 'parameter': 'voltage', 'value': 2.0}    # write to PSU voltage
r = requests.post(url, json=data)
print(r.json())

data = {'operation': 'write', 'parameter': 'current', 'value': 2.0}    # write to PSU current
r = requests.post(url, json=data)
print(r.json())

data = {'operation': 'write', 'parameter': 'ocp', 'value': True}       # psu OCP on
r = requests.post(url, json=data)
print(r.json())

data = {'operation': 'write', 'parameter': 'output', 'value': True}    # psu on/off
r = requests.post(url, json=data)
print(r.json())

time.sleep(0.5)  # wait for output to stabilize before attempting a read

data = {'operation': 'read', 'parameter': 'voltage'}   # read voltage
r = requests.post(url, json=data)
print(r.json())

data = {'operation': 'read', 'parameter': 'current'}   # read current
r = requests.post(url, json=data)
print(r.json())

data = {'operation': 'read', 'parameter': 'status'}   # read status
r = requests.post(url, json=data)
print(r.json())

data = {'operation': 'reset'}   # reset
r = requests.post(url, json=data)
print(r.json())
