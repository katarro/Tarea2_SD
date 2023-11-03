import getpass
from kafka_utils import connect_db

def ver_stock_ingredientes(id_maestro):
    connection = connect_db()
    if connection is None:
        return
    cursor = connection.cursor()
    
    query = "SELECT i.nombre, si.stock FROM StockIngredientes si JOIN Ingredientes i ON si.id_ingrediente = i.id WHERE si.id_maestro = %s"
    cursor.execute(query, (id_maestro,))
    rows = cursor.fetchall()
    
    if not rows:
        print("No tienes ingredientes en stock.")
    else:
        print("Stock de ingredientes:")
        for row in rows:
            print(f"{row[0]}: {row[1]}")
    
    cursor.close()
    connection.close()

def vender(id_maestro):
    connection = connect_db()
    if connection is None:
        return
    cursor = connection.cursor()
    
    # Mostrar los postres disponibles
    query = "SELECT id, nombre, precio FROM Postres"
    cursor.execute(query)
    postres = cursor.fetchall()
    
    if not postres:
        print("No hay postres disponibles para vender.")
        return
    
    print("Postres disponibles para vender:")
    for postre in postres:
        print(f"{postre[0]}. {postre[1]} - ${postre[2]}")
    
    id_postre = int(input("Ingresa el ID del postre a vender: "))
    
    # Verificar si hay suficiente stock de cada ingrediente
    query = """
    SELECT ip.id_ingrediente, i.nombre, ip.cantidad, si.stock
    FROM IngredientesPostre ip
    JOIN Ingredientes i ON ip.id_ingrediente = i.id
    LEFT JOIN StockIngredientes si ON ip.id_ingrediente = si.id_ingrediente AND si.id_maestro = %s
    WHERE ip.id_postre = %s
    """
    cursor.execute(query, (id_maestro, id_postre))
    ingredientes = cursor.fetchall()
    
    for ingrediente in ingredientes:
        if ingrediente[3] is None or ingrediente[3] < ingrediente[2]:
            print(f"No hay suficiente stock de {ingrediente[1]} para vender este postre.")
            return
    
    # Actualizar el stock de ingredientes
    for ingrediente in ingredientes:
        query = "UPDATE StockIngredientes SET stock = stock - %s WHERE id_maestro = %s AND id_ingrediente = %s"
        cursor.execute(query, (ingrediente[2], id_maestro, ingrediente[0]))
    
    # Registrar la venta
    query = "INSERT INTO Ventas (id_maestro, fecha, monto) VALUES (%s, CURRENT_DATE, (SELECT precio FROM Postres WHERE id = %s))"
    cursor.execute(query, (id_maestro, id_postre))
    
    connection.commit()
    print("Venta realizada con éxito.")
    
    cursor.close()
    connection.close()

def menu_maestro(id_maestro):
    while True:
        print("\nMenú del Maestro")
        print("1. Ver stock de ingredientes")
        print("2. Realizar venta")
        print("3. Salir")
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            ver_stock_ingredientes(id_maestro)
        elif opcion == "2":
            vender(id_maestro)
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Por favor elige una opción del 1 al 3.")

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
        query = "SELECT id, password FROM maestros WHERE email = %s AND aprobado = true"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            id_maestro, stored_password = result
            if password == stored_password:
                print("Ingreso exitoso!")
                menu_maestro(id_maestro)
            else:
                print("Contraseña incorrecta.")
        else:
            print("Usuario no encontrado o no está aprobado.")

        # Cerrar conexión
        cursor.close()
        connection.close()
    except Exception as e:
        print("Ocurrió un error:", str(e))
