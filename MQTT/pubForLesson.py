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
    # 定義連接成功後的回調函數
    def on_connect(client, userdata, flags, rc):
        print("已連接，結果代碼：{0}".format(rc))

    # 創建 MQTT 客戶端對象並設置連接成功時的回調函數
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    
    # 連接到 MQTT 代理（指定代理地址和端口）
    client.connect(host=broker, port=port)
    
    # 啟動 MQTT 客戶端的消息循環
    client.loop_start()
    
    # 定義要發布的消息內容和主題
    msg = "Message from MQTT"
    result = client.publish(topic=topic, payload=msg)
    
    # 打印發布消息的狀態和內容
    print("發布狀態：{0}\n發布消息：{1}".format(result[0], msg))
    
    # 停止 MQTT 客戶端的消息循環
    client.loop_stop()

if __name__ == '__main__':
    Main()