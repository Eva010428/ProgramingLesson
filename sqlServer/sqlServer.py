#%% 引入必要的資料庫模組
import pymysql
import pandas as pd
#%% 連線至MySQL資料庫
# 資料庫連線參數設定
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "root",
    "db": "company",
    "charset": "utf8"
}

try:
    # 嘗試與資料庫連線並創建游標
    conn = pymysql.connect(**db_settings)
    cursor = conn.cursor()
    
    print("連線成功")
except Exception as ex:
    print("連線失敗 : {}".format(ex))
#%% 使用 INSERT 語句初始化資料表
# 從 CSV 檔案中讀取員工資料
employeeData = pd.read_csv("Employee.csv")

try:
    # 遍歷每一筆員工資料
    for idx in range(employeeData.shape[0]):
        data = employeeData.iloc[idx, :]
        employeeId = data.iloc[0]
        education = data.iloc[1]
        joiningYear = data.iloc[2]
        city = data.iloc[3]
        paymentTier = data.iloc[4]
        age = data.iloc[5]
        gender = data.iloc[6]
    
        # 將員工資料插入到資料表中
        command = "INSERT INTO employee(ID, Education, JoiningYear, City, PaymentTier, Age, Gender) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(command, (employeeId, education, joiningYear, city, paymentTier, age, gender))
    
    # 提交資料表的變更
    conn.commit()
    print("INSERT語句執行成功")
except Exception as ex:
    print("錯誤 : {}".format(ex))
#%% 使用 SELECT 語句進行查詢
try:
    # 找出入職年份早於 2013 年且年齡大於 40 歲的員工
    command = "SELECT * FROM employee WHERE JoiningYear < 2013 AND Age > 40;"
    cursor.execute(command)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
    print("SELECT語句執行成功")
except Exception as ex:
    print("錯誤 : {}".format(ex))  
#%% 使用 UPDATE 語句更新資料並使用 SELECT 語句確認是否更新成功
try:
    # 更新 ID 為 3219 的員工的 PaymentTier
    cursor.execute("UPDATE employee SET PaymentTier = 3 WHERE ID = 3219;")
    conn.commit()
    print("UPDATE語句執行成功")
    
    # 查詢 ID 為 3219 的員工的數據
    cursor.execute("SELECT * FROM employee WHERE ID = 3219;")
    result = cursor.fetchone()
    print("查詢結果 : {0}".format(result))
except Exception as ex:
    print("錯誤 : {}".format(ex))  
#%% 使用 DELETE 語句刪除資料並使用 SELECT 語句確認是否刪除成功
try:   
    # 刪除入職年份早於 2013 年且年齡大於 40 歲的員工
    cursor.execute("DELETE FROM employee WHERE JoiningYear < 2013 AND Age > 40;")
    conn.commit()
    print("DELETE語句執行成功")
    
    # 查詢入職年份早於 2015 年且年齡大於 40 歲的員工
    cursor.execute("SELECT * FROM employee WHERE Age > 40 AND JoiningYear < 2015;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
   
except Exception as ex:
    print("錯誤 : {}".format(ex))
    #%% 計算年齡平均值、最大值和最小值
try:
    cursor.execute("SELECT AVG(Age) FROM employee;")
    employeeAgeMean = cursor.fetchone()
    cursor.execute("SELECT MAX(Age) FROM employee;")
    employeeAgeMax = cursor.fetchone()
    cursor.execute("SELECT MIN(Age) FROM employee;")
    employeeAgeMin = cursor.fetchone()
    cursor.execute("SELECT STD(Age) FROM employee;")
    employeeAgeSTD = cursor.fetchone()
    print("平均值 : {0};\n最大值 : {1};\n最小值 : {2};\n標準差 : {3};".format(employeeAgeMean, employeeAgeMax, employeeAgeMin, employeeAgeSTD))
except Exception as ex:
    print("錯誤 : {}".format(ex))   
#%% 查詢教育程度的不重複值並統計每個程度的人數   
try:
    cursor.execute("SELECT DISTINCT Education FROM employee;")
    educationTypes = cursor.fetchall()
    for educationType in educationTypes:
        cursor.execute("SELECT COUNT(Age) FROM employee WHERE PaymentTier = 2 AND Education = %s;", educationType)
        employeeCount = cursor.fetchone()
        print("教育程度 : {0}; 人數 : {1}".format(educationType, employeeCount))
except Exception as ex:
    print("錯誤 : {}".format(ex))   
#%%使用 DELETE 語句清空資料表
try:
    cursor.execute("DELETE FROM employee;")
    conn.commit()
    print("完成清空資料表")
except Exception as ex:
    print("錯誤 : {}".format(ex))   
#%% 確保資料庫連線關閉
conn.close()
print("關閉連線")