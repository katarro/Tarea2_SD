from flask import Flask, render_template, request, redirect, url_for
from confluent_kafka import Producer
import json

app = Flask(__name__)

def kafka_producer_config():
    conf = {
        'bootstrap.servers': 'kafka1:9092',  # Usamos el nombre del servicio del broker Kafka.
        'client.id': 'flask-app'
    }
    return Producer(conf)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = {
            'name': request.form['name'],
            'address': request.form['address'],
            'phone': request.form['phone'],
            'type': request.form['type']
        }
        
        message = json.dumps(form_data)
        
        producer = kafka_producer_config()
        producer.produce('FormularioInscripcion', value=message)
        producer.flush()
        
        return redirect(url_for('index'))
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Asegúrate de escuchar en todas las interfaces.
