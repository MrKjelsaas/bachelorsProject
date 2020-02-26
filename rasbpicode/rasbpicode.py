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

"""

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# Fixing random state for reproducibility
np.random.seed(19680801)


def Gen_RandLine(length, dims=2):
    # Create a line using a random walk algorithm

    # length is the number of points for the line.
    # dims is the number of dimensions the line has.

    lineData = np.empty((dims, length))
    lineData[:, 0] = np.random.rand(dims)
    for index in range(1, length):
        # scaling the random numbers by 0.1 so
        # movement is small compared to position.
        # subtraction by 0.5 is to change the range to [-0.5, 0.5]
        # to allow a line to move backwards.
        step = ((np.random.rand(dims) - 0.5) * 0.1)
        lineData[:, index] = lineData[:, index - 1] + step

    return lineData


def update_lines(num, dataLines, lines):
    for line, data in zip(lines, dataLines):
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(data[0:2, :num])
        line.set_3d_properties(data[2, :num])
    return lines

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Fifty lines of random 3-D lines
data = [Gen_RandLine(25, 3) for index in range(50)]

# Creating fifty line objects.
# NOTE: Can't pass empty arrays into 3d version of plot()
lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]

# Setting the axes properties
ax.set_xlim3d([0.0, 1.0])
ax.set_xlabel('X')

ax.set_ylim3d([0.0, 1.0])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, 1.0])
ax.set_zlabel('Z')

ax.set_title('3D Test')

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_lines, 25, fargs=(data, lines),
                                   interval=50, blit=False)

plt.show()

"""
