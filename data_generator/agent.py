import datetime
import json
import random
import time

def get_data():
    return {
        'EVENT_TIME': datetime.datetime.now().isoformat(),
        'TICKER': random.choice(['AAPL', 'AMZN', 'MSFT', 'INTC', 'TBV']),
        'PRICE': round(random.random() * 100, 2)}

def generate():
    f = open('/tmp/app.log','w')
    while True:
        time.sleep(1)
        data = json.dumps(get_data())
        print(data)
        f.write(data)

if __name__ == '__main__':
    generate()