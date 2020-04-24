import numpy as np
import scipy.optimize as sp

class logReg:
    def hypothesis(theta, X):
        return np.dot(theta, X)

    def sigmoid(x):
        return 1/ (1 + (np.exp(-x)) )

    def cost(theta, X, y, lambdaRegulator = 0):
        m = np.ma.size(y, 0)
        J = 0
        z = logReg.hypothesis(X, theta)
        h = logReg.sigmoid(z)

        J = (1/m) * (np.dot(-y.T, np.log(h)) - np.dot((1-y).T, np.log(1-h)) )
        J = J + (lambdaRegulator/(2*m)) * sum(theta[1:]) ** 2
        return float(J)

    def gradient(theta, X, y, lambdaRegulator = 0):
        m = np.ma.size(y, 0)
        grad = np.zeros(m)
        z = np.dot(X, theta)
        h = logReg.sigmoid(z)
        theta_regulator = theta
        theta_regulator[0] = 0

        grad = (1/m) * (np.dot(h - y.T, X)) + ((lambdaRegulator/m)*theta_regulator)
        return grad.T

    def predict(theta, X, threshold = 0.5):
        z = logReg.hypothesis(theta, X.T)
        h = logReg.sigmoid(z)

        for i in range(np.size(h)):
            if h[i] >= threshold:
                h[i] = 1
            else:
                h[i] = 0
        return h

    def oneVsAll(X, y, number_of_labels, lambdaRegulator = 0, maxIterations = 500):
        m = np.size(X, 0)
        n = np.size(X, 1)
        all_thetas = np.zeros([number_of_labels, n])
        initial_theta = np.zeros([n, 1])

        for c in range(number_of_labels):
            y_temp = np.zeros(np.shape(y))
            for i in range(np.size(y_temp, 0)):
                if y[i] == c:
                    y_temp[i] = 1
            all_thetas[c, :] = sp.fmin_cg(logReg.cost, initial_theta, fprime=logReg.gradient, args=(X, y_temp, lambdaRegulator), maxiter = maxIterations, disp = 0)

        return all_thetas

    def predictOneVsAll(all_thetas, X):
        m = np.size(X, 0)
        prediction = np.zeros([m, 1])

        predictions = logReg.sigmoid(logReg.hypothesis(all_thetas, X.T)).T
        for i in range(m):
            prediction[i] = np.argmax(predictions[i, :])

        return prediction

class neuralNetwork:
    def sigmoid_derivative(z):
        g = np.zeros(z.shape)
        g = logReg.sigmoid(z) * (1-logReg.sigmoid(z))
        return g
