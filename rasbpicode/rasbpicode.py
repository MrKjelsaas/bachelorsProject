# This is the code for the Raspberry Pi

import numpy as np
import time

def sensorReading(): # Dummy sensor reading from -1 to +1
    return 2*np.random.random() - 1
def currentDateTimeInPureNumbers(): # Returns format ddmmyyyy hhmmss
    string = time.strftime('%d/%m/%Y %H:%M:%S')
    date = string[0] + string[1]
    month = string[3] + string[4]
    year = string[6] + string[7] + string[8] + string[9]
    hour = string[11] + string[12]
    minute = string[14] + string[15]
    second = string[17] + string[18]
    dateStamp = date + month + year + " " + hour + minute + second
    return dateStamp

sensorReadingFrequency = 60


dataFilePath = "rasbpicode\\SavedData\\"
dataFileName = "Log for " + currentDateTimeInPureNumbers() + ".dat"
dataFileFullName = dataFilePath + dataFileName
print("Saving file as:", dataFileFullName, "\n")


data = np.zeros((0, 2)) # Left column is time of recording (since beginning), right column is the input value
startTime = time.time()


with open(dataFileFullName, 'wb') as file:
    for i in range(10):
        inputData = np.array([time.time()-startTime, sensorReading()])
        data = np.r_[data, [inputData]]

        np.savetxt(file, inputData)
        file.flush()

        time.sleep(1/sensorReadingFrequency)



print(data)
print("\nRecorded a total of", data.shape[0], "entries")








# At the beginning of the program
    # Establish connection to arduino and prepare to read signals
    # Create .dat file to save data to
        # Get a proper name and date



# The main loop
    # Read signals
    # Save signals
    # Check for break-trigger (button?)



# The closing of the program
    # Save all data
    # Close .dat file
