import requests

"""
find all attached devices
"""
r = requests.post('http://localhost:5001/attached')
print('attached: ', r.json())

# get the first thermocouple attached
device_reference = r.json()['thermocouple'][0]
url = 'http://localhost:5001/thermocouple/{}'.format(device_reference)

'''
read from channel 0 of /thermocouple/TC-08
'''
data = {'channel': 0}
r = requests.post(url, json=data)
print(r.json())

'''
read from channels 0 and 4 of /thermocouple/TC-08
'''
data = [{'channel': 0}, {'channel': 4}]
r = requests.post(url, json=data)
print(r.json())
