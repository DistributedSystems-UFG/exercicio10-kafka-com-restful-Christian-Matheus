from kafka import KafkaConsumer
from const import *
import threading
import datetime

from flask import Flask, jsonify

app = Flask(__name__)
history = []

@app.route('/latest')
def get_latest():
    if len(history) == 0:
        return jsonify({'average': 0.0, 'timestamp': 'No data yet'})
    last = history[-1]
    return jsonify(last)

@app.route('/history')
def get_history():
    return jsonify(history)

def consume():
    consumer = KafkaConsumer(bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT])
    consumer.subscribe(['topic-average'])

    print('Listening on topic-average...')

    for msg in consumer:
        average = float(msg.value.decode())
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        history.append({'average': average, 'timestamp': timestamp})
        print('Stored average: ' + str(average) + ' at ' + timestamp)

if __name__ == '__main__':
    t = threading.Thread(target=consume)
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', port=5000)
