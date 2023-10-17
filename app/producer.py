from flask import Flask, render_template, request
import json
from kafka import KafkaProducer

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers=['kafka1:9092', 'kafka2:9093', 'kafka3:9094'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'address': request.form['address'],
            'phone': request.form['phone'],
            'type': request.form['type']
        }
        producer.send('my-topic', value=data)
        return "Datos enviados!"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
