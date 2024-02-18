import json
import time
import requests
from kafka import KafkaProducer

def get_velib_data():
    """
    Get velib data from api
    :return: list of stations information
    """
    response = requests.get('https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json')
    data = json.loads(response.text)

    stations = data["data"]["stations"]

    filtered_stations = [station for station in stations if station["stationCode"] in ["16107", "32017"]]

    return filtered_stations


def velib_producer():
    """
    Create a producer to write velib data in kafka
    :return:
    """
    producer = KafkaProducer(bootstrap_servers="localhost:9092",
                             value_serializer=lambda x: json.dumps(x).encode('utf-8')
                             )

    while True:
        data = get_velib_data()
        for message in data:
            producer.send("velib-projet", message)
            print("added:", message)
        time.sleep(1)


if __name__ == '__main__':
    velib_producer()
