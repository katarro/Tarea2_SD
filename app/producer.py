from confluent_kafka import KafkaError, KafkaException, Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic
import psycopg2
import getpass
import json
import os
import select
import sys


producer = Producer({'bootstrap.servers': 'kafka1:9092,kafka2:9093,kafka3:9094'})
admin_client = AdminClient({'bootstrap.servers': 'kafka1:9092,kafka2:9093,kafka3:9094'})

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
    connection = psycopg2.connect(
        dbname="mamochi",
        user="mamochi",
        password="mamochi",
        host="db",  # Asegúrate de que este es el nombre correcto del servicio en tu docker-compose.yml
        port="5432"
    )
    cursor = connection.cursor()

    # Insertar los datos en la tabla correspondiente
    table_name = topic
    query = f"INSERT INTO {table_name} (name, address, phone, type, password, email) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (data['name'], data['address'], data['phone'], data['type'], data['password'], data['email']))
    connection.commit()

    # Cerrar conexión
    cursor.close()
    connection.close()
def main_menu():
    while True:
        print("\nBienvenido a Mamochi")
        print("1. Registrarse")
        print("2. Ingresar")
        print("3. Administrador")
        print("4. Salir")
        choice = input("Elige una opción: ")
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            admin()
        elif choice == "4":
            print("Hasta luego!")
            break
        else:
            print("Opción no válida, por favor elige una opción del 1 al 4.")

def register():
    print("\nRegistro de Usuario")
    data = {
        'name': input("Nombre: "),
        'address': input("Dirección: "),
        'phone': input("Teléfono: "),
        'type': input("Tipo (regular_topic/paid_topic): "),
        'password': input("Contraseña: "),
        'email': input("Correo electrónico: ")
    }
    send_data_to_kafka(data)

def login():
    print("\nIngreso de Usuario")
    email = input("Correo electrónico: ")
    password = getpass.getpass("Contraseña: ")  # Usar getpass para ocultar la contraseña mientras se escribe

    # Establecer conexión con la base de datos
    connection = psycopg2.connect(
        dbname="mamochi",
        user="mamochi",
        password="mamochi",
        host="db",  # Asegúrate de que este es el nombre correcto del servicio en tu docker-compose.yml
        port="5432"
    )
    cursor = connection.cursor()

    # Buscar al usuario por correo electrónico en regular_topic
    query = "SELECT password FROM regular_topic WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()

    if result:
        stored_password = result[0]
        if password == stored_password:
            print("Ingreso exitoso!")
            cursor.close()
            connection.close()
            return
        else:
            print("Contraseña incorrecta.")
            cursor.close()
            connection.close()
            return

    # Si no se encuentra en regular_topic, buscar en paid_topic
    query = "SELECT password FROM paid_topic WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()

    if result:
        stored_password = result[0]
        if password == stored_password:
            print("Ingreso exitoso!")
        else:
            print("Contraseña incorrecta.")
    else:
        print("Usuario no encontrado.")

    # Cerrar conexión
    cursor.close()
    connection.close()

########3
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


##########
def admin():
    print("\nPanel de Administrador")

    consumer = create_consumer()

    while True:
        print("1. Ver mensajes del tópico 'regular_topic'")
        print("2. Ver mensajes del tópico 'paid_topic'")
        print("3. Salir")
        choice = input("Elige una opción: ")

        if choice == "1":
            consume_topic(consumer, 'regular_topic')
        elif choice == "2":
            consume_topic(consumer, 'paid_topic')
        elif choice == "3":
            print("Saliendo del Panel de Administrador.")
            break
        else:
            print("Opción no válida, por favor elige una opción del 1 al 3.")

    consumer.close()
    print("\nFin de la información de administrador")

if __name__ == "__main__":
    main_menu()
