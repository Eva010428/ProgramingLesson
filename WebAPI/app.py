#%% 匯入必要的模組
from flask import Flask
from flask_restful import Resource, Api

#%% 建立 Flask 應用程式及庫存初始化
app = Flask(__name__)

# 建立 RESTful API 物件
api = Api(app)

# 建立一個簡單的資料儲存，包含產品(Product)和材料(Material-a, Material-b, Material-c)的數量
storage = [
    {"Name" : "Product-A", "Amounts": 0},
    {"Name" : "Material-A", "Amounts": 10},
    {"Name" : "Material-B", "Amounts": 10},
    {"Name" : "Material-C", "Amounts": 10}
]

#%% 定義一個繼承自 Resource 的 HelloWorld 類別，處理根路徑的 GET 請求
class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello World!"}

#%% 定義一個繼承自 Resource 的 Storage 類別，處理 /storage 路徑的 GET 請求
class Storage(Resource):
    def get(self):
        return {"storage": storage}

#%% 定義一個繼承自 Resource 的 StorageManagement 類別，處理 /storage/<string:name>/<int:amounts> 路徑的 GET、POST、DELETE、PUT 請求
class StorageManagement(Resource):
    def get(self, name, amounts):
        for material in storage:
            if material["Name"] == name:
                return material
        return {"note": "找不到指定物料"}, 404

    def post(self, name, amounts):
        material = {
            "Name": name,
            "Amounts": amounts
        }
        storage.append(material)
        return {"note": "成功新增"}

    def delete(self, name, amounts):
        for idx in range(len(storage)):
            material = storage[idx]
            if material["Name"] == name:
                storage.pop(idx)
                return {"note": "成功刪除"}
        return {"note": "找不到指定物料"}, 404

    def put(self, name, amounts):
        materialFind = None
        for material in storage:
            if material["Name"] == name:
                materialFind = material
              
        if materialFind:
            storage.remove(materialFind)
            materialFind["Amounts"] = amounts
            storage.append(materialFind)
            return materialFind
        else:
            return {"note": "找不到指定物料"}, 404

#%% 產品製造
class ProductionManagement(Resource):
    def post(self, name, amounts):
        if "Product" not in name:
            return {"note": "指定物料並非產品"}
        
        for material in storage:
            if material["Name"] == name:
                break
        else:
            return {"note": "查無該產品"}
        
        errorCode = self._production(name,amounts)
        if errorCode == 0:
            return {"note": "製造完成"}
        elif errorCode == -1:
            return {"note": "倉庫內查無原物料"}
        elif errorCode == -2:
            return {"note": "原物料數量不足"}
            
    def _production(self,name,amounts):
        currentProductIdx = None
        currentMaterialAIdx= None
        for idx in range(len(storage)):
            material = storage[idx]
            if material["Name"] == name:
                currentProductIdx = idx
            if material["Name"] == "Material-A":
                currentMaterialAIdx= idx
            
            if currentProductIdx != None and currentMaterialAIdx!= None:
                break
        else:
            return -1
        
        currentMaterialAAmounts = storage[currentMaterialAIdx]["Amounts"] - amounts * 1
        if currentMaterialAAmounts < 0:
            return -2
        else:
            storage[currentProductIdx]["Amounts"] += amounts
            storage[currentMaterialAIdx]["Amounts"] = currentMaterialAAmounts
            return 0
            
#%% 將 HelloWorld、Storage、StorageManagement 類別加入 API 路由
api.add_resource(HelloWorld, "/")
api.add_resource(Storage, "/storage")
api.add_resource(StorageManagement, "/storage/<string:name>/<int:amounts>")
api.add_resource(ProductionManagement, "/production/<string:name>/<int:amounts>")

#%% 啟動應用程式，監聽在本地主機的端口 5000
app.run(host="localhost", port=5000, debug=False)
