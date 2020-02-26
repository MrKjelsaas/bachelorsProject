# This is the code for the Raspberry Pi

import numpy as np
from numpy import pi # So I only have to write pi instead of np.pi
import time
import matplotlib.pyplot as plt
import robotteknikk as rob




def sensorReading():  # Dummy sensor reading from 0 to 360
    return 360*np.random.random()
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


sensorReadingFrequency = 60


# Prepares the file name and path for data log
dataFilePath = "rasbpicode\\SavedData\\"
dataFileName = "Log for " + currentDateTimeInPureNumbers() + ".dat"
dataFileFullName = dataFilePath + dataFileName
print("Saving log as:", dataFileFullName, "\n")


"""
# Make a process for finding the baseline
baselineMeasurements = np.empty(100)
for n in range(100):
    baselineMeasurements[n] = sensorReading()

print(np.average(baselineMeasurements))
print(np.std(baselineMeasurements))
"""



data = np.empty((0, 4))  # Left column is time of recording (since beginning), right column is the input value
startTime = time.time()

with open(dataFileFullName, 'wb') as file:
    for i in range(100):
        inputData = np.array([time.time()-startTime, sensorReading(), sensorReading(), sensorReading()])
        data = np.r_[data, [inputData]]

        np.savetxt(file, inputData)
        file.flush()

        # time.sleep(1/sensorReadingFrequency)

# print(data)
print("\nRecorded a total of", data.shape[0], "entries")




fig1 = plt.figure()
ax = fig1.gca(projection='3d')
ax.set_xlim3d(-1, 1)
ax.set_ylim3d(-1, 1)
ax.set_zlim3d(-1, 1)
orientation = np.eye(4)
roll = 0
pitch = 0
yaw = 0
orientation[:3,:3] = rob.rpy2rotmat(roll, pitch, yaw)


plt.ion()
plotWidth = 35
for i in range(35):
    if i < plotWidth:
        ax = fig1.gca(projection='3d')
        ax.set_xlim3d(-1, 1)
        ax.set_ylim3d(-1, 1)
        ax.set_zlim3d(-1, 1)
        roll += 0
        pitch += pi/35
        yaw += 0
        orientation[:3,:3] = rob.rpy2rotmat(roll, pitch, yaw)

        rob.trplot3(ax, orientation)
        plt.draw()
        plt.pause(0.01)
        plt.clf()


    else:
        ax = fig1.gca(projection='3d')
        ax.set_xlim3d(-1, 1)
        ax.set_ylim3d(-1, 1)
        ax.set_zlim3d(-1, 1)
        roll += 0
        pitch += 0
        yaw += 0
        orientation[:3,:3] = rob.rpy2rotmat(roll, pitch, yaw)

        rob.trplot3(ax, orientation)
        plt.draw()
        plt.pause(0.01)
        plt.clf()




# At the beginning of the program
    # Establish connection to arduino and prepare to read signals
    # Create .dat file to save data to
        # Get a proper name and date
    # Find baseline for masurements to determine initial position (standing still)



# The main loop
    # Read signals
    # Save signals
    # Check for break-trigger (button?)



# The closing of the program
    # Save all data
    # Close .dat file
