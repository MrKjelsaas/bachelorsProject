
import numpy as np
import matplotlib.pyplot as plt
import MLfunctions as ml
import scipy.optimize as sp
import time

lambdaRegulator = 0.01
hidden_layer_size = 50
number_of_labels = 2

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

X = np.c_[np.ones([m, 1]), X]
weights1 = ml.neuralNetwork.randInitializeWeights(n, hidden_layer_size)
weights2 = ml.neuralNetwork.randInitializeWeights(hidden_layer_size, number_of_labels)

prediction = ml.neuralNetwork.predict(weights1, weights2, X)
