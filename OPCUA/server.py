#%%引入模組
import time
import random as rnd
from opcua import Server
#%% 創建一個 OPC UA 伺服器，設定命名空間並取得伺服器上的物件節點
server = Server()
server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")

uri = "http://examples.freeopcua.github.io"
idx = server.register_namespace(uri)

objects = server.get_objects_node()
#%% 建立客廳物件資料夾
folderLivingRoom = objects.add_object(idx, "LivingRoom")

# 建立客廳各個變數節點
nodeTimeStampLivingRoom = folderLivingRoom.add_variable(idx, "TimeStamp", 0)
nodeTemperatureSensorLivingRoom = folderLivingRoom.add_variable(idx, "Temperature Sensor", 0)
nodeHumiditySensorLivingRoom = folderLivingRoom.add_variable(idx, "Humidity Sensor", 0)
nodeLightSensorLivingRoom = folderLivingRoom.add_variable(idx, "Light Sensor", False)
nodeLightActuatorLivingRoom = folderLivingRoom.add_variable(idx, "Light Switch", False)

# 設定可寫入的變數
nodeLightActuatorLivingRoom.set_writable()
#%%在客廳資料夾額外建立一個冷氣機節點
nodeConditionerActuatorLivingRoom = folderLivingRoom.add_variable(idx, "Conditioner Switch", False)
nodeConditionerTemperatureLivingRoom = folderLivingRoom.add_variable(idx, "Conditioner Temperature", 0)

# 設定可寫入的變數
nodeConditionerTemperatureLivingRoom.set_writable()
nodeConditionerActuatorLivingRoom.set_writable()
#%% 啟動伺服器
server.start()

try:
    while True:
        time.sleep(1)
        currentTime = time.strftime("%m/%d/%Y : %H:%M:%S")
        currentTemperature = 25 + rnd.uniform(-0.2, 0.2)
        currentHumidity = 0.5 + rnd.uniform(-0.05, 0.05)

        if nodeConditionerActuatorLivingRoom.get_value() == True:
            currentTemperature = nodeConditionerTemperatureLivingRoom.get_value() + rnd.uniform(-0.1, 0.1)

        # 更新各節點的值
        nodeTimeStampLivingRoom.set_value(currentTime)
        nodeTemperatureSensorLivingRoom.set_value(currentTemperature)
        nodeHumiditySensorLivingRoom.set_value(currentHumidity)

        if nodeLightActuatorLivingRoom.get_value() == True:
            nodeLightSensorLivingRoom.set_value(True)
        else:
            nodeLightSensorLivingRoom.set_value(False)

finally:
    # 關閉伺服器
    server.stop()
