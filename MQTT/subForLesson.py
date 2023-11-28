import random
from paho.mqtt import client as mqtt_client



# MQTT代理的地址和端口
broker = 'broker.emqx.io'
port = 1883

# 要訂閱的主題
topic = "ITRI/MQTTtest"

# 生成一個隨機的客戶端ID
client_id = f'subscribe-{random.randint(0, 100)}'

def Main():
    # 定義連接成功時的回調函數
    def on_connect(client, userdata, flags, rc):
        print("已連接，結果代碼：{0}".format(rc))

    # 定義消息到達時的回調函數
    def on_message(client, userdata, msg):
        print(f"接收到來自 `{msg.topic}` 主題的消息：`{msg.payload.decode()}`")

    # 創建 MQTT 客戶端對象
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message

    # 連接到 MQTT 代理
    client.connect(host=broker, port=port)

    # 訂閱指定主題
    client.subscribe(topic)

    # 啟動 MQTT 客戶端的消息循環，等待消息到達
    client.loop_forever()

if __name__ == '__main__':
    Main()