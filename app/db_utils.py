from kafka_utils import send_data_to_kafka



def register_maestro():
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


# Aquí puedes agregar más funciones para interactuar con la base de datos
