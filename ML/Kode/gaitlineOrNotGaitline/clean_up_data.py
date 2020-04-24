
import numpy as np
import os

with_shoes_directory = r"C:\Users\magnu\OneDrive\Skole\Bacheloroppgaven\ML\Kode\gaitlineOrNotGaitline\data\with_shoes"
without_shoes_directory = r"C:\Users\magnu\OneDrive\Skole\Bacheloroppgaven\ML\Kode\gaitlineOrNotGaitline\data\without_shoes"

m = len(os.listdir(with_shoes_directory)) + len(os.listdir(without_shoes_directory))

# Enter the number of parameters here:
n = 3
data = np.zeros([m, n+1])

files_iterated = 0
for filename in os.listdir(with_shoes_directory):
    if filename.endswith(".dat"):
        dataFile = np.loadtxt(os.path.join(with_shoes_directory, filename))
        data[files_iterated, 0] = np.std(dataFile[:, 1])
        data[files_iterated, 1] = np.std(dataFile[:, 2])
        data[files_iterated, 2] = np.mean(dataFile[:, 1])
        data[files_iterated, n] = 1
        files_iterated += 1

for filename in os.listdir(without_shoes_directory):
    if filename.endswith(".dat"):
        dataFile = np.loadtxt(os.path.join(without_shoes_directory, filename))
        data[files_iterated, 0] = np.std(dataFile[:, 1])
        data[files_iterated, 1] = np.std(dataFile[:, 2])
        data[files_iterated, 2] = np.mean(dataFile[:, 1])
        data[files_iterated, n] = 0
        files_iterated += 1

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
            data = np.delete(data, (i), axis=0)
        if data[i, j] > (mean[j] + (3*std[j])):
            data = np.delete(data, (i), axis=0)
    i += 1

# Normalize the data
for i in range(n):
    data[:, i] -= min(data[:, i])
    data[:, i] /= max(data[:, i])
    # Every data input is now a number between 0 and 1

np.random.shuffle(data)
training_data = data[:int(np.size(data, 0)*0.8), :]
test_data = data[int(np.size(data, 0)*0.8):, :]

np.savetxt(r"C:\Users\magnu\OneDrive\Skole\Bacheloroppgaven\ML\Kode\gaitlineOrNotGaitline\data\training_data.dat", training_data)
np.savetxt(r"C:\Users\magnu\OneDrive\Skole\Bacheloroppgaven\ML\Kode\gaitlineOrNotGaitline\data\test_data.dat", test_data)
