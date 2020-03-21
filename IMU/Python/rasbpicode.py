# This is the code for the Raspberry Pi

import numpy as np
from numpy import pi # So I only have to write pi instead of np.pi
import time
import threading
import serial

def currentDateTimeInPureNumbers():  # Returns format ddmmyyyy hhmmss
    string = time.strftime('%d/%m/%Y %H:%M:%S')
    date = string[0] + string[1]
    month = string[3] + string[4]
    year = string[6] + string[7] + string[8] + string[9]
    hour = string[11] + string[12]
    minute = string[14] + string[15]
    second = string[17] + string[18]
    dateStamp = date + month + year + " " + hour + minute + second
    return dateStamp
def toRadian(degrees):
    return degrees*(pi/180)
def getSensorData():
    b = ser.readline()         # read a byte string
    string = b.decode()        # decode byte string into Unicode
    string = string.rstrip()   # remove \n and \r
    string = string.split(',') # makes a list of the values
    roll = float(string[0])
    pitch = float(string[1])
    yaw = float(string[2])
    return roll, pitch, yaw

ser = serial.Serial(port='COM6', baudrate=115200)
time.sleep(2)

# Prepares the file name and path for data log
dataFilePath = "SavedData\\"
dataFileName = "Log for " + currentDateTimeInPureNumbers() + ".dat"
dataFileFullName = dataFilePath + dataFileName
print("Saving log as:", dataFileFullName, "\n")

"""
Todo:
Make a thread to detect keypress so that data collection stops when that key is pressed
Put data reading in a while loop (for example while(dataCollectionDone == 0))
"""

data = np.empty((0, 4))  # Left column is time of recording (since beginning), right column is the input value

print("Starting data collection...")
startTime = time.time()
for i in range(1000):
    x, y, z = getSensorData()
    inputData = np.array([time.time()-startTime, x, y, z])
    data = np.r_[data, [inputData]]
    if i % 100 == 0:
        if i != 0:
            print("Recorded " + str(i) + " entries so far")

np.savetxt(dataFileFullName, data)

print("\nRecorded a total of", data.shape[0], "entries")




# Start program
# Give patient a few seconds to start walking
# Record data for a certain time (30 seconds?)
# Save data
