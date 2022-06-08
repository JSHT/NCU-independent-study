# Dependencies
# sktime: 0.9.0
# scikit-learn: 0.24.2
# numpy: 1.19.3
# pandas 1.1.5
# joblib: 1.1.0
# adafruit-circuitpython-adxl34x 1.12.2

import time
from math import sqrt
import board
import serial
import busio
import adafruit_adxl34x

import joblib
import pandas as pd

# import time series random forest model+
model = joblib.load('modelwithML')

s = serial.Serial('/dev/ttyACM0', 115200)

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

accV = []
[xpre, ypre, zpre] = accelerometer.acceleration

while True:
    accV = []
    # judge "震度" every 2 seconds
    for i in range(19):
        # using adxl345 to get acceleration information
        [x, y, z] = accelerometer.acceleration
        tmpX = (x-xpre)*100
        tmpY = (y-ypre)*100
        tmpZ = (z-zpre)*100
        acc = sqrt((tmpX)**2+(tmpY)**2+(tmpZ)**2)  # cm/(s^2)
        accV.append(acc)
        [xpre, ypre, zpre] = [x, y, z]
        print([x, y, z])
        time.sleep(0.1)
    print('prediction')
    seismic = model.predict(pd.DataFrame([[pd.Series(accV)]]))[0]
    # send "震度" to Arduino
    s.write(str(seismic).encode())
    print(seismic)
