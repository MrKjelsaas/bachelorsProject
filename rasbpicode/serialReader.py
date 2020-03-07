import serial
import time


# set up serial line
ser = serial.Serial(port='COM4', baudrate=9600)
time.sleep(2)

# Read and record the data
data =[]                       # empty list to store the data
for i in range(50):
    b = ser.readline()         # read a byte string
    string = b.decode()        # decode byte string into Unicode
    string = string.rstrip()   # remove \n and \r
    string = string.split(',') # makes a list of the values
    roll = float(string[0])
    pitch = float(string[1])
    yaw = float(string[2])
    #flt = float(string)       # convert string to float
    print(roll, pitch, yaw)
    data.append(string)        # add to the end of data list
    time.sleep(0.1)            # wait (sleep) 0.1 seconds

ser.close()
