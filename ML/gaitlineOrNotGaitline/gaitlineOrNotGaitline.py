
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

# Initialize theta and add the 1-column to X
theta = np.ones(n+1)
X = np.c_[np.ones([m, 1]), X]
lambdaRegulator = 0.01
print("Using lambda regulator", lambdaRegulator, "\n")

if n == 2: # Plotting and visualizing the training data
    print("Visualizing data\nX represents y=0\nO represents y=1\n")
    fig = plt.figure()
    for i in range(m):
        if y[i] == 0:
            plt.scatter(X[i, 1], X[i, 2], color="r", marker="X")
        else:
            plt.scatter(X[i, 1], X[i, 2], color="b", marker="o")

    plt.xlim(min(X[:, 1] - 0.5), max(X[:, 1] + 0.5))
    plt.ylim(min(X[:, 2] - 0.5), max(X[:, 2] + 0.5))
    plt.title("Training data")
    plt.xlabel("X0")
    plt.ylabel("X1")
    plt.show()

print("Optimizing theta...")
theta = sp.fmin_cg(ml.logReg.cost, theta, fprime=ml.logReg.gradient, args=(X, y, lambdaRegulator), maxiter = 100)
print("\nOptimal theta: ", theta)

if n == 2: # Plotting and visualizing the decision boundary
    fig = plt.figure()
    for i in range(m):
        if y[i] == 0:
            plt.scatter(X[i, 1], X[i, 2], color="r", marker="X")
        else:
            plt.scatter(X[i, 1], X[i, 2], color="b", marker="o")
    x_plot = np.array([min(X[:, 1]), max(X[:, 1])])
    y_plot = (-1/theta[2]) * (theta[1] * x_plot + theta[0])
    plt.xlim(min(X[:, 1] - 0.5), max(X[:, 1] + 0.5))
    plt.ylim(min(X[:, 2] - 0.5), max(X[:, 2] + 0.5))
    plt.title("Training data with decision boundary")
    plt.xlabel("X0")
    plt.ylabel("X1")
    plt.plot(x_plot, y_plot)
    plt.show()

try: # Load test data
    test_data = np.loadtxt(r"data\test_data.dat")
    m = np.shape(test_data)[0]
    n = np.shape(test_data)[1] - 1
    X_test = np.zeros([m, n])
    y_test = np.zeros(m)
    X_test = test_data[:, :n]
    y_test = test_data[:, n]
    print("\nSuccessfully loaded", m, "entries\n")
except:
    print("Error loading data, now exiting...")
    time.sleep(3)
    exit()
X_test = np.c_[np.ones([m, 1]), X_test]

# Calculate model accuracy
prediction = ml.logReg.predict(theta, X_test)
accuracy = prediction == y_test
accuracy = 100*(sum(accuracy)/np.size(y_test))
print("\nTest data accuracy:      %.2f" % accuracy, "%", sep='')
prediction = ml.logReg.predict(theta, X)
accuracy = prediction == y
accuracy = 100*(sum(accuracy)/np.size(y))
print("Training data accuracy:  %.2f" % accuracy, "%", sep='')

if n == 2: # Plotting and visualizing the data
    fig = plt.figure()
    for i in range(np.size(y_test)):
        if y_test[i] == 0:
            plt.scatter(X_test[i, 1], X_test[i, 2], color="r", marker="X")
        else:
            plt.scatter(X_test[i, 1], X_test[i, 2], color="b", marker="o")
    x_plot = np.array([min(X_test[:, 1]), max(X_test[:, 1])])
    y_plot = (-1/theta[2]) * (theta[1] * x_plot + theta[0])
    plt.xlim(min(X[:, 1] - 0.5), max(X[:, 1] + 0.5))
    plt.ylim(min(X[:, 2] - 0.5), max(X[:, 2] + 0.5))
    plt.title("Test data with decision boundary")
    plt.xlabel("X0")
    plt.ylabel("X1")
    plt.plot(x_plot, y_plot)
    plt.show()

print("\n\nEnd of program")
