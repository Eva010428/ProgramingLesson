# -*- coding: utf-8 -*-
import random
from paho.mqtt import client as mqtt_client



broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'subscribe-{random.randint(0, 100)}'

def ExampleCode():
    def connect_mqtt():
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(client_id)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client

    def subscribe(client: mqtt_client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        client.subscribe(topic)
        client.on_message = on_message
            
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    ExampleCode()

