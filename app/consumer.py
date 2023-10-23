from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'regular_topic',
    'paid_topic',
    bootstrap_servers=['kafka1:9092', 'kafka2:9093', 'kafka3:9094'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

data = {
    'regular_topic': [],
    'paid_topic': []
}

for message in consumer:
    data[message.topic].append(message.value)
    print(f"Received message: {message.value} from topic: {message.topic}")
