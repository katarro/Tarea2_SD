import getpass
from kafka_utils import connect_db

def login():
    print("\nIngreso de Usuario")
    email = input("Correo electrónico: ")
    password = getpass.getpass("Contraseña: ")  # Usar getpass para ocultar la contraseña mientras se escribe

    # Establecer conexión con la base de datos
    connection = connect_db()
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

