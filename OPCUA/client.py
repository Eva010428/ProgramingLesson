#%% 引入模組
from opcua import Client
#%% 建立客戶端並嘗試連線
client = Client("opc.tcp://localhost:4840/freeopcua/server/")
try:
    client.connect()
    print("連線成功建立")
except Exception as ex:
    print("連線失敗: {0}.".format(ex))
#%% 瀏覽目前節點狀況
try:
    folderLivingRoom = client.get_node("ns=2;i=1").get_children()
    for child in folderLivingRoom:
        nodeId = child.nodeid
        nodeDisplayName = child.get_display_name().Text
        nodeValue = child.get_value()
        print("節點 ID:{0};顯示名稱:{1};數值:{2}".format(nodeId, nodeDisplayName, nodeValue))
except Exception as ex:
    print("連線錯誤: {0}".format(ex))
#%% 開啟電燈
try:
    nodeLightActuator = client.get_node("ns=2;i=6")
    nodeLightActuator.set_value(True)
    print("完成")
except Exception as ex:
    print("連線錯誤: {0}".format(ex))
#%% 設定冷氣並開啟
try:
    nodeConditionerTemperature = client.get_node("ns=2;i=8")
    nodeConditionerTemperature.set_value(22)
    nodeConditionerActuator = client.get_node("ns=2;i=7")
    nodeConditionerActuator.set_value(True)
    print("完成")
except Exception as ex:
    print("連線錯誤: {0}".format(ex))
#%% 設定唯讀節點
try:
    nodeTemperature = client.get_node("ns=2;i=3")
    nodeTemperature.set_value(20)
    print("完成")
except Exception as ex:
    print("連線錯誤: {0}".format(ex))
#%% 關閉連線
client.disconnect()
