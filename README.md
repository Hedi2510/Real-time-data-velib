# Real-time-data-velib
TP project individuel 

1)Creation des topic : 
./kafka_2.12-2.6.0/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --
partitions 1 --topic velib-projet


./kafka_2.12-2.6.0/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --
partitions 1 --topic velib-projet-final-data


2)Collecte des données des stations vélibs 
stations filtré 


3)filtrage de donnée
Modification de la section kafka join pour rajouter le code postal du fichier csv 

création d'un nouveau dataframe (dataframe_out)
