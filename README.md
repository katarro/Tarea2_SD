# Tarea2_SD

## Pasos
0. docker-compose down
1. docker-compose build
2. docker-compose up -d
<<<<<<< HEAD

## ¿Cómo ver el fomulario enviado?
=======

## ¿Cómo ver el fomulario enviado?

0. Ingresar al contenedor: docker exec -it "nombre contenedor" /bin/bash


## Crear topico
0. kafka-topics.sh --create --bootstrap-server kafka1:9092 --replication-factor 1 --partitions 1 --topic "nombre topico"

## Listar Topicos
0. kafka-topics.sh --list --bootstrap-server kafka1:9092

## Eliminar Topico
0. kafka-topics.sh --delete --bootstrap-server kafka1:9092 --topic "nombre topico"

## Listar contenido de un Topico
1. kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic regular-topic --from-beginning
2. kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic paid-topic --from-beginning

>>>>>>> bfe1244 (V1.0)

0. Ingresar al contenedor: docker exec -it "nombre contenedor" /bin/bash


## Crear topico
0. kafka-topics.sh --create --bootstrap-server kafka1:9092 --replication-factor 1 --partitions 1 --topic "nombre topico"

## Listar Topicos
0. kafka-topics.sh --list --bootstrap-server kafka1:9092

## Eliminar Topico
0. kafka-topics.sh --delete --bootstrap-server kafka1:9092 --topic "nombre topico"

## Listar contenido de un Topico
1. kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic regular-topic --from-beginning
2. kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic paid-topic --from-beginning


## Abrir base de datos
1. sudo docker exec -it "contenedor" psql -U mamochi mamochi