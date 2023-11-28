import random
import time

from paho.mqtt import client as mqtt_client



broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'publish-{random.randint(0, 1000)}'

def ExampleMain():
    def Connect_mqtt():
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        
        client = mqtt_client.Client(client_id)
        # 左側是一個屬性，而右側是將一個方法直接賦予該屬性。因此不需要括號(以方法的方式呼叫)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client


    def Publish(client):
        msg_count = 1
        while True:
            time.sleep(1)
            msg = f"messages: {msg_count}"
            result = client.publish(topic, msg)
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
            msg_count += 1
            if msg_count > 5:
                break
    
    client = Connect_mqtt()
    client.loop_start()
    Publish(client)
    client.loop_stop()

if __name__ == '__main__':
    ExampleMain()