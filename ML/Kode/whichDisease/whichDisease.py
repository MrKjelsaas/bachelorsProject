
import numpy as np
import matplotlib.pyplot as plt
import MLfunctions as ml
import scipy.optimize as sp
import time



try: # Load training data
    training_data = np.loadtxt(r"data\training_data.dat")
    m = np.shape(training_data)[0]
    n = np.shape(training_data)[1] - 1
    X = np.zeros([m, n])
    y = np.zeros(m)
    X = training_data[:, :n]
    y = training_data[:, n]
    print("\nSuccessfully loaded", m, "entries\n")
except:
    print("Error loading data, now exiting...")
    time.sleep(3)
    exit()

thetas = np.ones(n+1)
X = np.c_[np.ones([m, 1]), X]
lambdaRegulator = 0.01
print("Using lambda regulator", lambdaRegulator, "\n")


thetas = ml.logReg.oneVsAll(X, y, 2, lambdaRegulator = lambdaRegulator, maxIterations = 1000)

predictions = ml.logReg.predictOneVsAll(thetas, X)

sum = 0
for i in range(np.size(y)):
    if predictions[i] == y[i]:
        sum += 1
accuracy = 100*(sum/np.size(y))
print("\nTraining data accuracy:  %.2f" % accuracy, "%", sep='')


try: # Load training data
    test_data = np.loadtxt(r"data\test_data.dat")
    m = np.shape(test_data)[0]
    n = np.shape(test_data)[1] - 1
    X_test = np.zeros([m, n])
    y_test = np.zeros(m)
    X = test_data[:, :n]
    y = test_data[:, n]
    print("\nSuccessfully loaded", m, "entries\n")
except:
    print("Error loading data, now exiting...")
    time.sleep(3)
    exit()
X_test = np.c_[np.ones([m, 1]), X_test]

predictions = ml.logReg.predictOneVsAll(thetas, X_test)

sum = 0
for i in range(np.size(y_test)):
    if predictions[i] == y[i]:
        sum += 1
accuracy = 100*(sum/np.size(y_test))
print("\nTest data accuracy:  %.2f" % accuracy, "%", sep='')
