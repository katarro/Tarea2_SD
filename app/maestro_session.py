import getpass
from kafka_utils import connect_db

def login():
    print("\nIngreso de Usuario")
    email = input("Correo electrónico: ")
    password = getpass.getpass("Contraseña: ")  # Usar getpass para ocultar la contraseña mientras se escribe

    try:
        # Establecer conexión con la base de datos
        connection = connect_db()
        if connection is None:
            return
        cursor = connection.cursor()

        # Buscar al usuario por correo electrónico en maestros
        query = "SELECT password FROM maestros WHERE email = %s AND aprobado = true"

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
    except Exception as e:
        print("Ocurrió un error:", str(e))