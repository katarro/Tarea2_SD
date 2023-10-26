import kafka_utils
import funciones
import db_utils
import maestro_session

def ver_datos_tabla(tabla):
    connection = kafka_utils.connect_db()
    cursor = connection.cursor()
    query = f"SELECT * FROM {tabla}"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    connection.close()

def admin():
    print("\nPanel de Administrador")

    consumer = kafka_utils.create_consumer()

    while True:
        print("\n1. Ver mensajes del tópico 'regular_topic'")
        print("2. Ver mensajes del tópico 'paid_topic'")
        print("3. Gestionar Maestros")
        print("4. Gestionar Stock de Ingredientes")
        print("5. Ver Ventas de Maestros")
        print("6. Salir")
        choice = input("Elige una opción: ")

        if choice == "1":
            ver_datos_tabla('regular_topic')
        elif choice == "2":
            ver_datos_tabla('paid_topic')
        elif choice == "3":
            gestionar_maestros()
        elif choice == "4":
            gestionar_stock_ingredientes()
        elif choice == "5":
            ver_ventas_maestros()
        elif choice == "6":
            print("Saliendo del Panel de Administrador.")
            break
        else:
            print("Opción no válida, por favor elige una opción del 1 al 6.")

    consumer.close()
    print("\nFin de la información de administrador")

def gestionar_maestros():
    while True:
        print("\n1. Aprobar Maestro")
        print("2. Rechazar Maestro")
        print("3. Ver Lista de Maestros")
        print("4. Salir")
        choice = input("Elige una opción: ")
        if choice == "1":
            funciones.aprobar_maestro()
        elif choice == "2":
            funciones.rechazar_maestro()
        elif choice == "3":
            funciones.ver_lista_maestros()
        elif choice == "4":
            break
        else:
            print("Opción no válida, por favor elige una opción del 1 al 4.")


def gestionar_stock_ingredientes():
    while True:
        print("\n1. Agregar Stock")
        print("2. Ver Stock de Ingredientes")
        print("3. Salir")
        choice = input("Elige una opción: ")
        if choice == "1":
            funciones.agregar_stock()
        elif choice == "2":
            funciones.ver_stock_ingredientes()
        elif choice == "3":
            break
        else:
            print("Opción no válida, por favor elige una opción del 1 al 4.")


def ver_ventas_maestros():
    connection = kafka_utils.connect_db()
    cursor = connection.cursor()
    query = "SELECT * FROM ventas"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    connection.close()

def menu():
    while True:
        print("\nBienvenido a Mamochi")
        print("1. Registrarse como Maestro")
        print("2. Iniciar Sesión")
        print("3. Panel de Administrador")
        print("4. Salir")
        choice = input("Elige una opción: ")

        if choice == "1":
            db_utils.register_maestro()
        elif choice == "2":
            maestro_session.login()
        elif choice == "3":
            admin()
        elif choice == "4":
            print("Hasta luego!")
            break
        else:
            print("Opción no válida, por favor elige una opción del 1 al 4.")


if __name__ == "__main__":
    menu()
