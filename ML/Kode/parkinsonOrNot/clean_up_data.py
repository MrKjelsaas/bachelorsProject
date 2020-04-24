
import numpy as np
from scipy import stats
import os
import threading

with_parkinson_directory = r"data\with_parkinson"
without_parkinson_directory = r"data\without_parkinson"

m = len(os.listdir(with_parkinson_directory)) + len(os.listdir(without_parkinson_directory))

# Enter the number of parameters here:
n = 7
data = np.zeros([m, n+1])

# Extraction of data
def grabWithParkinsonData():
    print("Collecting data from", with_parkinson_directory)
    files_iterated = 0
    for filename in os.listdir(with_parkinson_directory):
        dataFile = np.loadtxt(os.path.join(with_parkinson_directory, filename))
        forceIsZeroLeft = 0
        forceIsZeroRight = 0
        for i in range(np.size(dataFile, 0)):
            if dataFile[i, 17] == 0:
                forceIsZeroLeft += 1
            elif dataFile[i, 18] == 0:
                forceIsZeroRight += 1
        data[files_iterated, 0] = forceIsZeroLeft/np.size(dataFile, 0)
        data[files_iterated, 1] = forceIsZeroRight/np.size(dataFile, 0)
        data[files_iterated, 2] = stats.variation(dataFile[:, 17])
        data[files_iterated, 3] = stats.variation(dataFile[:, 18])
        data[files_iterated, 4] = np.mean(dataFile[:, 17]) - np.mean(dataFile[:, 18])
        data[files_iterated, 5] = np.std(dataFile[:, 17]) - np.std(dataFile[:, 18])
        data[files_iterated, 6] = data[files_iterated, 0] / data[files_iterated, 1]
        data[files_iterated, n] = 1
        files_iterated += 1
def grabWithoutParkinsonData():
    print("Collecting data from", without_parkinson_directory)
    files_iterated = len(os.listdir(with_parkinson_directory))
    for filename in os.listdir(without_parkinson_directory):
        dataFile = np.loadtxt(os.path.join(without_parkinson_directory, filename))
        forceIsZeroLeft = 0
        forceIsZeroRight = 0
        for i in range(np.size(dataFile, 0)):
            if dataFile[i, 17] == 0:
                forceIsZeroLeft += 1
            elif dataFile[i, 18] == 0:
                forceIsZeroRight += 1
        data[files_iterated, 0] = forceIsZeroLeft/np.size(dataFile, 0)
        data[files_iterated, 1] = forceIsZeroRight/np.size(dataFile, 0)
        data[files_iterated, 2] = stats.variation(dataFile[:, 17])
        data[files_iterated, 3] = stats.variation(dataFile[:, 18])
        data[files_iterated, 4] = np.mean(dataFile[:, 17]) - np.mean(dataFile[:, 18])
        data[files_iterated, 5] = np.std(dataFile[:, 17]) - np.std(dataFile[:, 18])
        data[files_iterated, 6] = data[files_iterated, 0] / data[files_iterated, 1]
        data[files_iterated, n] = 0
        files_iterated += 1

withoutParkinsonData = threading.Thread(target=grabWithoutParkinsonData)
withoutParkinsonData.start()
withParkinsonData = threading.Thread(target=grabWithParkinsonData)
withParkinsonData.start()

withParkinsonData.join()
withoutParkinsonData.join()

# Remove any entry that is beyond 3 standard deviations from the mean
mean = np.zeros(n-1)
std = np.zeros(n-1)
for i in range(n-1):
    mean[i] = np.mean(data[:, i])
    std[i] = np.std(data[:, i])
i = 0
while (i < np.size(data, 0)):
    for j in range(n-1):
        if data[i, j] < (mean[j] - (3*std[j])):
            data = np.delete(data, i, axis=0)
            i -= 1
        if data[i, j] > (mean[j] + (3*std[j])):
            data = np.delete(data, i, axis=0)
            i -= 1
    i += 1

# Normalize the data
for i in range(n):
    data[:, i] -= min(data[:, i])
    data[:, i] /= max(data[:, i])
    # Every data input is now a number between 0 and 1

np.random.shuffle(data)
training_data = data[:int(np.size(data, 0)*0.8), :]
test_data = data[int(np.size(data, 0)*0.8):, :]

np.savetxt(r"data\training_data.dat", training_data)
np.savetxt(r"data\test_data.dat", test_data)
