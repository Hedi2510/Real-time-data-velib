# Real-time-data-velib
TP project individuel 
0)lancement : 

1. Démarrage de Zookeeper
./kafka_2.12-2.6.0/bin/zookeeper-server-start.sh ./kafka_2.12-2.6.0/config/zookeeper.properties

2. Démarrage du serveur Kafka
./kafka_2.12-2.6.0/bin/kafka-server-start.sh ./kafka_2.12-2.6.0/config/server.properties

3. Pour lancer un script appélé "producer.py" sur python sur un terminal
python producer.py

>1)Creation des topic :

TOPIC 1 : velib-projet
kafka-topics --create --topic velib-projet --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

TOPIC 2 : velib-projet-final-data
kafka-topics --create --topic velib-projet-final-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1


lire les msg 
/kafka_2.12-2.6.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic velib-projet -- from-beginning

>2)Collecte des données des stations vélibs 
stations filtré (16107 et 32017)
envoie des données vers topic vélib

>3)Spark : traitement

Modification de la section kafka join pour rajouter le code postal du fichier csv 

création d'un nouveau dataframe (dataframe_out)

