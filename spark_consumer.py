from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_json, struct
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType, MapType, TimestampType

import os
os.environ["SPARK_HOME"] = "/path/to/your/spark-3.2.3-bin-hadoop2.7"
os.environ["JAVA_HOME"] = "/path/to/your/java-11-openjdk-amd64"
import findspark
findspark.init()

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("VelibDataProcessing") \
        .master("local[1]") \
        .config("spark.sql.shuffle.partitions", "1") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.3") \
        .getOrCreate()

    schema = StructType([
        StructField("stationCode", StringType()),
        StructField("station_id", StringType()),
        StructField("num_bikes_available", IntegerType()),
        StructField("numBikesAvailable", IntegerType()),
        StructField("num_bikes_available_types", ArrayType(MapType(StringType(), IntegerType()))),
        StructField("num_docks_available", IntegerType()),
        StructField("numDocksAvailable", IntegerType()),
        StructField("is_installed", IntegerType()),
        StructField("is_returning", IntegerType()),
        StructField("is_renting", IntegerType()),
        StructField("last_reported", TimestampType())
    ])

    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "velib-projet") \
        .option("startingOffsets", "earliest") \
        .load() \
        .select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

    df_station_informations = spark.read.csv("stations_information.csv", header=True)

    enriched_df = kafka_df.join(df_station_informations, ["stationCode", "station_id"])

    indicators_df = enriched_df.groupBy("postcode").agg(
        sum("num_bikes_available").alias("total_bikes"),
        sum("mechanical").alias("total_mechanical_bikes"),
        sum("ebike").alias("total_ebikes")
    )

    output_df = indicators_df.select(to_json(struct("postcode", "total_bikes", "total_mechanical_bikes", "total_ebikes")).alias("value"))

    query = output_df.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "velib-projet-clean") \
        .option("checkpointLocation", "/path/to/checkpoint/dir") \
        .start()

    query.awaitTermination()
