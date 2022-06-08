# Dependencies
# MariaDB 1.0.9
# adafruit-circuitpython-adxl34x 1.12.2

import time
# using adxl345 to get acceleration data
import board
import busio
import adafruit_adxl34x

from mysql.connector import Error
import mysql.connector

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)


try:
    # 連接 MySQL/MariaDB 資料庫
    connection = mysql.connector.connect(
        host='localhost',   # 主機名稱
        database='data7',   # 資料庫名稱1
        user='pi',          # 帳號
        password='')        # 密碼

    # data1 ~ 10
    if connection.is_connected():

        # 顯示資料庫版本
        db_Info = connection.get_server_info()
        print("資料庫版本：", db_Info)
        sql = "INSERT INTO data (x, y, z) VALUES (%s, %s, %s);"
        cursor = connection.cursor()
        print("start")
        while(1):
            # 新增資料
            new_data = accelerometer.acceleration
            cursor.execute(sql, new_data)
            # 確認資料有存入資料庫
            connection.commit()
            # print(new_data)
            time.sleep(0.1)

except Error as e:
    print("資料庫連接失敗：", e)

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("資料庫連線已關閉")
