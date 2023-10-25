from kafka import KafkaConsumer
import json

class KafkaConsumerManager:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'regular_topic',
            'paid_topic',
            bootstrap_servers=['kafka1:9092', 'kafka2:9093', 'kafka3:9094'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        self.data = {
            'regular_topic': [],
            'paid_topic': []
        }

    def consume_messages(self):
        for message in self.consumer:
            self.data[message.topic].append(message.value)
            print(f"Received message: {message.value} from topic: {message.topic}")

# Crear una instancia de KafkaConsumerManager
kafka_consumer_manager = KafkaConsumerManager()

# Iniciar la consumición de mensajes en un hilo aparte si es necesario
