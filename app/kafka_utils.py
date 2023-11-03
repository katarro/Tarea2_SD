from confluent_kafka import KafkaError, KafkaException, Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic
import psycopg2
import json

producer = Producer({'bootstrap.servers': 'kafka1:9092,kafka2:9093,kafka3:9094'})
admin_client = AdminClient({'bootstrap.servers': 'kafka1:9092,kafka2:9093,kafka3:9094'})

def connect_db():
    try:
        # Configuración de la conexión a la base de datos
        connection = psycopg2.connect(
            dbname="mamochi",
            user="mamochi",
            password="mamochi",
            host="db",
            port="5432"
        )
        print("Conexión exitosa a la base de datos.")
        return connection
    except Exception as e:
        print(f"Error al conectar a la base de datos: {str(e)}")
        return None
    
def create_topic_if_not_exists(topic_name):
    metadata = admin_client.list_topics(timeout=10)
    topics = metadata.topics
    if topic_name not in topics:
        print(f"El tópico {topic_name} no existe. Creándolo...")
        new_topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)
        admin_client.create_topics([new_topic])
        print(f"Tópico {topic_name} creado con éxito.")
    else:
        print(f"El tópico {topic_name} ya existe.")

def send_data_to_kafka(data):
    topic = 'regular_topic' if data.get('type') == 'normal' else 'paid_topic'
    create_topic_if_not_exists(topic)
    
    try:
        producer.produce(topic, value=json.dumps(data).encode('utf-8'))
        producer.flush()  # Asegúrate de que todos los mensajes se envíen antes de continuar
        print(f"Datos enviados al tópico {topic}.")
    except Exception as e:
        print(f"Ocurrió un error al enviar los datos al tópico {topic}: {str(e)}")

    # Establecer conexión con la base de datos
    connection = connect_db()
    if connection is None:
        return
    try:
        cursor = connection.cursor()

        # Insertar los datos en la tabla correspondiente
        table_name = topic
        query = f"INSERT INTO {table_name} (name, address, phone, type, password, email) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (data['name'], data['address'], data['phone'], data['type'], data['password'], data['email']))
        connection.commit()
    except Exception as e:
        print(f"Ocurrió un error al insertar los datos en la base de datos: {str(e)}")
        connection.rollback()
    finally:
        # Cerrar conexión
        cursor.close()
        connection.close()

def create_consumer():
    conf = {
        'bootstrap.servers': 'kafka1:9092,kafka2:9093,kafka3:9094',  # Asegúrate de que estos son los nombres y puertos correctos de tus brokers de Kafka
        'group.id': 'my_group',
        'auto.offset.reset': 'earliest',
    }
    return Consumer(conf)

def consume_topic(consumer, topic):
    try:
        consumer.subscribe([topic])
        print(f"\nMensajes en el tópico {topic}:")

        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # Fin de la partición
                    continue
                elif msg.error().code() == KafkaError._ALL_BROKERS_DOWN:
                    print("Todos los brokers están abajo. Verifica tu conexión a Kafka.")
                    break
                else:
                    print("Error en Kafka:", msg.error())
                    break
            
            print('Mensaje:', msg.value().decode('utf-8'))

            # Verificar si hay una tecla presionada
            user_input = input("Presiona 'exit' para salir: ")
            if user_input.lower() == 'exit':
                break


    except KafkaException as ke:
        print("Error en Kafka:", str(ke))
    except Exception as e:
        print("Error inesperado:", str(e))
    finally:
        try:
            consumer.unsubscribe()
            consumer.close()
            print("Consumidor desconectado.")
        except RuntimeError:
            print("El consumidor ya estaba cerrado.")

