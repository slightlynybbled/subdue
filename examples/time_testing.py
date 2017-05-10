import requests
from datetime import datetime


def get():
    host = 'http://127.0.0.1:5001'

    start_time = datetime.now()
    r = requests.get(host)
    end_time = datetime.now()

    print('response: ', r.text)
    print('headers:', r.headers)
    print('timedelta', end_time - start_time)
    print()

get()
