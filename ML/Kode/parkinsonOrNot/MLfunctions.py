import numpy as np

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
