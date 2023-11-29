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

#%% 定義一個繼承自 Resource 的 ProductionManagement 類別，處理 /storage/<string:name>/<int:amounts> 路徑的 GET 請求
class ProductionManagement(Resource):
    def get(self, name, amounts):
        # 檢查指定物料是否為產品
        if "Product" not in name:
            return {"note": "指定物料並非產品"}
        
        # 在 recipes 中查找指定產品
        for product in recipes:
            if product["Name"] == name:
                break
        else:
            return {"note": "查無該產品"}
        
        # 調用 _production 方法進行製造，並根據回傳的錯誤碼提供相應的訊息
        errorCode = self._production(name, amounts)
        if errorCode == 0:
            return {"note": "製造完成"}
        elif errorCode == -1:
            return {"note": "倉庫內查無原物料"}
        elif errorCode == -2:
            return {"note": "原物料數量不足"}
            
    def _production(self, name, amounts):
        # 在 recipes 中找到指定產品的配方
        productRecipe = None
        for product in recipes:
            if product["Name"] == name:
                productRecipe = product
   
        # 檢查原物料庫存是否足夠
        for productMaterial in productRecipe["Recipe"]:
            for material in storage:
                if material["Name"] != productMaterial["Name"]:
                    continue
                
                if material["Amounts"] < amounts * productMaterial["Amounts"]:
                    return -2                
                break
            else:
                return -1
            
        # 扣除原物料庫存
        for productMaterial in productRecipe["Recipe"]:
            for material in storage:
                if material["Name"] == productMaterial["Name"]:
                    material["Amounts"] -= amounts * productMaterial["Amounts"]
                    break
                    
        # 更新產品庫存
        for material in storage:
            if material["Name"] == name:
                material["Amounts"] = amounts
                
        return 0
            
#%% 將 HelloWorld、Storage、StorageManagement 類別加入 API 路由
api.add_resource(HelloWorld, "/")
api.add_resource(Storage, "/storage")
api.add_resource(StorageManagement, "/storage/<string:name>/<int:amounts>")
api.add_resource(ProductionManagement, "/production/<string:name>/<int:amounts>")

#%% 啟動應用程式，監聽在本地主機的端口 5000
app.run(host="localhost", port=5000, debug=False)
