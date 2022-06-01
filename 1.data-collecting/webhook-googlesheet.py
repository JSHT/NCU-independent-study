import requests
import datetime
import time

import board
import busio
import adafruit_adxl34x

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)


while True:
    xv = []
    yv = []
    zv = []
    # collect data for 2 seconds
    for i in range(20):
        [x, y, z] = accelerometer.acceleration
        xv.append(x)
        yv.append(y)
        zv.append(z)
        time.sleep(0.1)

    data_to_send = {
        "x": xv,
        "y": yv,
        "z": zv,
        "ts": str(datetime.datetime.now()),
        "class": "0"
    }
    # print(data_to_send)

    url = ""  # Integromat Webhook URL
    r = requests.post(url, json=data_to_send)
    print(r.status_code)
    if(r.status_code == 200):
        print('資料已成功傳輸')
    else:
        print('failed')
