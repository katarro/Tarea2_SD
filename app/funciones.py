import psycopg2

def create_connection():
    connection = psycopg2.connect(
        dbname="mamochi",
        user="mamochi",
        password="mamochi",
        host="localhost",  # Cambia esto por la dirección de tu base de datos
        port="5432"
    )
    return connection

def aprobar_maestro():
    connection = create_connection()
    cursor = connection.cursor()
    
    id_maestro = input("Ingresa el ID del maestro a aprobar: ")
    query = "UPDATE maestros SET estado = 'aprobado' WHERE id = %s"
    cursor.execute(query, (id_maestro,))
    connection.commit()
    
    print("Maestro aprobado con éxito.")
    cursor.close()
    connection.close()

def rechazar_maestro():
    connection = create_connection()
    cursor = connection.cursor()
    
    id_maestro = input("Ingresa el ID del maestro a rechazar: ")
    query = "UPDATE maestros SET estado = 'rechazado' WHERE id = %s"
    cursor.execute(query, (id_maestro,))
    connection.commit()
    
    print("Maestro rechazado con éxito.")
    cursor.close()
    connection.close()

def ver_lista_maestros():
    connection = create_connection()
    cursor = connection.cursor()
    
    query = "SELECT * FROM maestros"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    cursor.close()
    connection.close()

def agregar_stock():
    connection = create_connection()
    cursor = connection.cursor()
    
    id_maestro = input("Ingresa el ID del maestro: ")
    id_ingrediente = input("Ingresa el ID del ingrediente: ")
    cantidad = input("Ingresa la cantidad a agregar: ")
    
    query = "UPDATE stock_ingredientes SET stock = stock + %s WHERE id_maestro = %s AND id_ingrediente = %s"
    cursor.execute(query, (cantidad, id_maestro, id_ingrediente))
    connection.commit()
    
    print("Stock agregado con éxito.")
    cursor.close()
    connection.close()

def reducir_stock():
    connection = create_connection()
    cursor = connection.cursor()
    
    id_maestro = input("Ingresa el ID del maestro: ")
    id_ingrediente = input("Ingresa el ID del ingrediente: ")
    cantidad = input("Ingresa la cantidad a reducir: ")
    
    query = "UPDATE stock_ingredientes SET stock = stock - %s WHERE id_maestro = %s AND id_ingrediente = %s"
    cursor.execute(query, (cantidad, id_maestro, id_ingrediente))
    connection.commit()
    
    print("Stock reducido con éxito.")
    cursor.close()
    connection.close()

def ver_stock_ingredientes():
    connection = create_connection()
    cursor = connection.cursor()
    
    query = "SELECT * FROM stock_ingredientes"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    cursor.close()
    connection.close()
