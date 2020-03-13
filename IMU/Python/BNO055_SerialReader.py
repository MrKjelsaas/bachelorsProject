# Python script that reads data from arduino with COM port 

import serial
import time

# set up serial line
arduinoData=serial.Serial('COM9',115200) # COM port and the baudrart has to match with the Arduino
time.sleep(1) # Delay with one second, making sure that the serial port has a chance to set up nicely

# while loop that reads the data
while(1==1): 
    while(arduinoData.inWaiting()==0): # Waiting until there's data 
        pass
    
    dataPacket=arduinoData.readline() # Read a byte string
    dataPacket=str(dataPacket,'utf-8') # Encode to right format. Removes b, \n and \r
    splitPacket=dataPacket.split(',') # Split the string into an array

    # Convert strings to floats. 
    
    # Calibration data. If the value is 0 = uncalibrated, if value is 3 = calibrated 
    Scal=float(splitPacket[0]) # Scal= System calibration 
    Gcal=float(splitPacket[1]) # Gcal= Gyroscope calibration
    Acal=float(splitPacket[2]) # Acal= Accelerometer calibration
    Mcal=float(splitPacket[3]) # Mcal= Magnetometer calibration

    # Orientation data
    Yaw=float(splitPacket[4])
    Pitch=float(splitPacket[5])
    Roll=float(splitPacket[6])
   
    #Prints the labels and the values
    print("Scal",Scal,"Gcal",Gcal,"Acal",Acal,"Mcal",Mcal,"Roll",Roll,"Pitch",Pitch,"Yaw",Yaw)   
