from kafka_utils import create_consumer, consume_topic

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
