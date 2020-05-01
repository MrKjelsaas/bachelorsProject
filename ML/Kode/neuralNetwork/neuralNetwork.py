
import numpy as np
import matplotlib.pyplot as plt
import MLfunctions as ml
import scipy.optimize as sp
import time

lambdaRegulator = 0.01
hidden_layer_size = 10
number_of_labels = 3
iterations = 100

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

weights1 = ml.neuralNetwork.randInitializeWeights(n, hidden_layer_size)
weights2 = ml.neuralNetwork.randInitializeWeights(hidden_layer_size, number_of_labels)
nn_parameters = np.zeros(np.size(weights1) + np.size(weights2))
nn_parameters[:np.size(weights1)] = weights1.flatten()
nn_parameters[np.size(weights1):] = weights2.flatten()

print("Training...")
args = (n, hidden_layer_size, X, y, number_of_labels, lambdaRegulator)
nn_parameters = sp.minimize(ml.neuralNetwork.cost, nn_parameters, args=args, method='Nelder-Mead')['x']
print("Training complete\n")

hypothesis = ml.neuralNetwork.hypothesis(nn_parameters, n, hidden_layer_size, X, number_of_labels)
prediction = ml.neuralNetwork.predict(nn_parameters, n, hidden_layer_size, X, number_of_labels)

sum = 0
for i in range(np.size(y)):
    if prediction[i] == y[i]:
        sum += 1
accuracy = 100*(sum/np.size(y))
print("Training data accuracy:  %.2f" % accuracy, "%", sep='')

try: # Load test data
    test_data = np.loadtxt(r"data\test_data.dat")
    m = np.shape(test_data)[0]
    n = np.shape(test_data)[1] - 1
    X = np.zeros([m, n])
    y = np.zeros(m)
    X = test_data[:, :n]
    y = test_data[:, n]
    print("\nSuccessfully loaded", m, "entries\n")
except:
    print("Error loading data, now exiting...")
    time.sleep(3)
    exit()

hypothesis = ml.neuralNetwork.hypothesis(nn_parameters, n, hidden_layer_size, X, number_of_labels)
prediction = ml.neuralNetwork.predict(nn_parameters, n, hidden_layer_size, X, number_of_labels)

sum = 0
for i in range(np.size(y)):
    if prediction[i] == y[i]:
        sum += 1
accuracy = 100*(sum/np.size(y))
print("Test data accuracy:  %.2f" % accuracy, "%", sep='')
