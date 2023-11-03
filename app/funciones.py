import psycopg2
import kafka_utils

def create_connection():
    try:
        return kafka_utils.connect_db()
    except psycopg2.OperationalError as e:
        print("Error al conectar a la base de datos:", str(e))
        return None

def eliminar_mensaje_kafka(id_maestro, topico):
    # Logica
    print(f"Mensaje del maestro con ID {id_maestro} eliminado del tópico {topico}.")


def aprobar_maestro():
    try:
        connection = create_connection()
        if connection is None:
            return
        cursor = connection.cursor()
        
        id_maestro = input("Ingresa el ID del maestro a aprobar: ")
        topico = input("Ingresa el nombre del tópico (regular_topic/paid_topic): ").lower()
        
        if topico not in ['regular_topic', 'paid_topic']:
            print("Nombre de tópico inválido. Debe ser 'regular_topic' o 'paid_topic'.")
            return
        
        # Obtener información del maestro
        query = f"SELECT * FROM {topico} WHERE id = %s"
        cursor.execute(query, (id_maestro,))
        maestro = cursor.fetchone()
        
        if maestro is None:
            print("Maestro no encontrado.")
            return
        
        # Aprobar maestro y moverlo a la tabla maestros
        query = "INSERT INTO maestros (name, address, phone, type, password, email, aprobado) VALUES (%s, %s, %s, %s, %s, %s, true)"
        cursor.execute(query, (maestro[1], maestro[2], maestro[3], maestro[4], maestro[5], maestro[6]))
        
        # Eliminar maestro de la tabla original
        query = f"DELETE FROM {topico} WHERE id = %s"
        cursor.execute(query, (id_maestro,))
        
        connection.commit()
        print("Maestro aprobado con éxito.")
        
        # Eliminar mensaje de Kafka
        eliminar_mensaje_kafka(id_maestro, topico)
        
        cursor.close()
        connection.close()
    except Exception as e:
        print("Ocurrió un error:", str(e))


def rechazar_maestro():
    try:
        connection = create_connection()
        if connection is None:
            return
        cursor = connection.cursor()
        
        id_maestro = input("Ingresa el ID del maestro a rechazar: ")
        topico = input("Ingresa el nombre del tópico (regular_topic/paid_topic): ").lower()
        
        if topico not in ['regular_topic', 'paid_topic']:
            print("Nombre de tópico inválido. Debe ser 'regular_topic' o 'paid_topic'.")
            return
        
        # Obtener información del maestro
        query = f"SELECT * FROM {topico} WHERE id = %s"
        cursor.execute(query, (id_maestro,))
        maestro = cursor.fetchone()
        
        if maestro is None:
            print("Maestro no encontrado.")
            return
        
        # Rechazar maestro y moverlo a la tabla maestros
        query = "INSERT INTO maestros (name, address, phone, type, password, email, aprobado) VALUES (%s, %s, %s, %s, %s, %s, false)"
        cursor.execute(query, (maestro[1], maestro[2], maestro[3], maestro[4], maestro[5], maestro[6]))
        
        # Eliminar maestro de la tabla original
        query = f"DELETE FROM {topico} WHERE id = %s"
        cursor.execute(query, (id_maestro,))
        
        connection.commit()
        print("Maestro rechazado con éxito.")
        
        cursor.close()
        connection.close()
    except Exception as e:
        print("Ocurrió un error:", str(e))


def ver_lista_maestros():
    try:
        connection = create_connection()
        if connection is None:
            return
        cursor = connection.cursor()
        
        print("\nMaestros en regular_topic:")
        query = "SELECT * FROM regular_topic"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        
        print("\nMaestros en paid_topic:")
        query = "SELECT * FROM paid_topic"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        print("\nMaestros aprobados:")
        query = "SELECT * FROM Maestros WHERE aprobado = TRUE"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if not rows:
            print("No hay maestros aprobados.")
        else:
            for row in rows:
                print(row)
        
        cursor.close()
        connection.close()
    except Exception as e:
        print("Ocurrió un error:", str(e))

# Aquí puedes agregar las demás funciones según sea necesario

def agregar_stock():
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()

    try:

        print("\nMaestros aprobados:")
        query = "SELECT * FROM Maestros WHERE aprobado = TRUE"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if not rows:
            print("No hay maestros aprobados.")
        else:
            for row in rows:
                print(row)

        # Pedir la información al usuario
        id_maestro = input("Ingresa el ID del maestro: ")
        nombre_ingrediente = input("Ingresa el nombre del ingrediente: ")
        cantidad = int(input("Ingresa la cantidad de stock a agregar: "))

        # Verificar si el ingrediente existe
        query = "SELECT id FROM Ingredientes WHERE nombre = %s"
        cursor.execute(query, (nombre_ingrediente,))
        resultado = cursor.fetchone()
        if resultado is None:
            print("El ingrediente no existe.")
            return
        id_ingrediente = resultado[0]

        # Verificar si ya existe stock para ese maestro e ingrediente
        query = "SELECT stock FROM StockIngredientes WHERE id_maestro = %s AND id_ingrediente = %s"
        cursor.execute(query, (id_maestro, id_ingrediente))
        resultado = cursor.fetchone()

        if resultado is None:
            # Si no existe, insertar el nuevo stock
            query = "INSERT INTO StockIngredientes (id_maestro, id_ingrediente, stock) VALUES (%s, %s, %s)"
            cursor.execute(query, (id_maestro, id_ingrediente, cantidad))
        else:
            # Si ya existe, actualizar el stock existente
            query = "UPDATE StockIngredientes SET stock = stock + %s WHERE id_maestro = %s AND id_ingrediente = %s"
            cursor.execute(query, (cantidad, id_maestro, id_ingrediente))

        connection.commit()
        print("Stock agregado con éxito.")

    except Exception as e:
        print("Ocurrió un error:", str(e))
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

def ver_stock_ingredientes():
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()

    # Solicitar al usuario el nombre del postre
    nombre_postre = input("Ingresa el nombre del postre: ")

    try:
        # Consultar el stock de ingredientes para el postre especificado
        query = """
        SELECT p.nombre as postre, i.nombre as ingrediente, ip.cantidad
        FROM IngredientesPostre ip
        JOIN Postres p ON ip.id_postre = p.id
        JOIN Ingredientes i ON ip.id_ingrediente = i.id
        WHERE p.nombre = %s;
        """
        cursor.execute(query, (nombre_postre,))
        rows = cursor.fetchall()

        if not rows:
            print("No se encontraron ingredientes para el postre especificado.")
        else:
            print("\nStock de ingredientes para:", nombre_postre)
            for row in rows:
                print(f"{row[1]}: {row[2]} unidades")

    except Exception as e:
        print("Ocurrió un error al consultar el stock de ingredientes:", str(e))

    finally:
        cursor.close()
        connection.close()
