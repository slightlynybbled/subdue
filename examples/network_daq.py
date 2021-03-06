import time
import requests

"""
find all attached devices
"""
r = requests.post('http://localhost:5001/attached')
print('attached: ', r.json())

# get the first DAQ attached
device_reference = r.json()['daq'][0]
url = 'http://localhost:5001/daq/{}'.format(device_reference)

'''
write 'high' to /Dev1/port0/line0
'''
data = {
    'operation': 'do',
    'port': 0,
    'line': 0,
    'value': 1
}
requests.post(url, json=data)
time.sleep(1.0)

data['value'] = 0
requests.post(url, json=data)


'''
read /Dev1/port0/line1 (digital)
'''

data = {
    'operation': 'di',
    'port': 0,
    'line': 1
}
r = requests.post(url, json=data)

print(r.json())  # print out the returned JSON data

'''
write 1.25V, then 1.75V to ao0
'''
data = {
    'operation': 'ao',
    'ao': 0,
    'value': 1.25
}
requests.post(url, json=data)

time.sleep(1.0)
data['value'] = 1.75
requests.post(url, json=data)

'''
read from ai0
'''
data = {
    'operation': 'ai',
    'ai': 0
}
r = requests.post(url, json=data)
print(r.json())

'''
execute a series of commands
'''
time.sleep(1.0)
data = [
    {'operation': 'ao', 'ao': 0, 'value': 1.25},
    {'operation': 'ai', 'ai': 0},
    {'operation': 'ao', 'ao': 0, 'value': 1.75},
    {'operation': 'ai', 'ai': 0},
    {'operation': 'ao', 'ao': 0, 'value': 2.25},
    {'operation': 'ai', 'ai': 0}
]
r = requests.post(url, json=data)
print(r.json())
