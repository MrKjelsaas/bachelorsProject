import numpy as np
import scipy.optimize as sp

def sigmoid(x):
    return 1/ (1 + (np.exp(-x)) )

class logReg:
    def hypothesis(theta, X):
        return np.dot(theta, X)

    def cost(theta, X, y, lambdaRegulator = 0):
        m = np.ma.size(y, 0)
        J = 0
        z = logReg.hypothesis(X, theta)
        h = sigmoid(z)

        J = (1/m) * (np.dot(-y.T, np.log(h)) - np.dot((1-y).T, np.log(1-h)) )
        J = J + (lambdaRegulator/(2*m)) * sum(theta[1:]) ** 2
        return float(J)

    def gradient(theta, X, y, lambdaRegulator = 0):
        m = np.ma.size(y, 0)
        grad = np.zeros(m)
        z = np.dot(X, theta)
        h = sigmoid(z)
        theta_regulator = theta
        theta_regulator[0] = 0

        grad = (1/m) * (np.dot(h - y.T, X)) + ((lambdaRegulator/m)*theta_regulator)
        return grad.T

    def predict(theta, X, threshold = 0.5):
        z = logReg.hypothesis(theta, X.T)
        h = sigmoid(z)

        for i in range(np.size(h)):
            if h[i] >= threshold:
                h[i] = 1
            else:
                h[i] = 0
        return h

    def oneVsAll(X, y, number_of_labels, lambdaRegulator = 0, maxIterations = 1000):
        n = np.size(X, 1)
        all_thetas = np.zeros([number_of_labels, n])
        initial_theta = np.zeros([n, 1])

        for c in range(number_of_labels):
            y_temp = np.zeros(np.shape(y))
            for i in range(np.size(y_temp, 0)):
                if y[i] == c:
                    y_temp[i] = 1
            all_thetas[c, :] = sp.fmin_cg(logReg.cost, initial_theta, fprime=logReg.gradient, args=(X, y_temp, lambdaRegulator), maxiter = maxIterations, disp=0)
        return all_thetas

    def predictOneVsAll(all_thetas, X):
        m = np.size(X, 0)
        prediction = np.zeros([m, 1])

        predictions = sigmoid(logReg.hypothesis(all_thetas, X.T)).T
        for i in range(m):
            prediction[i] = np.argmax(predictions[i, :])
        return prediction

class neuralNetwork:
    def sigmoid_derivative(z):
        return sigmoid(z) * (1-sigmoid(z))

    def hypothesis(nn_parameters, input_layer_size, hidden_layer_size, X, number_of_labels):
        Theta1 = nn_parameters[:hidden_layer_size * (input_layer_size + 1)].reshape(hidden_layer_size, input_layer_size+1)
        Theta2 = nn_parameters[hidden_layer_size * (input_layer_size + 1):].reshape(number_of_labels, hidden_layer_size+1)
        m = np.size(X, 0)
        X = np.c_[np.ones([m, 1]), X]

        z2 = np.dot(Theta1, X.T)
        a2 = sigmoid(z2).T
        a2 = np.c_[np.ones([np.size(a2, 0), 1]), a2]
        z3 = np.dot(Theta2, a2.T)
        a3 = sigmoid(z3).T
        return a3

    def predict(nn_parameters, input_layer_size, hidden_layer_size, X, number_of_labels):
        m = np.size(X, 0)
        X = np.c_[np.ones([m, 1]), X]
        prediction = np.zeros([m, 1])
        Theta1 = nn_parameters[:hidden_layer_size * (input_layer_size + 1)].reshape(hidden_layer_size, input_layer_size+1)
        Theta2 = nn_parameters[hidden_layer_size * (input_layer_size + 1):].reshape(number_of_labels, hidden_layer_size+1)

        z2 = np.dot(Theta1, X.T)
        a2 = sigmoid(z2).T
        a2 = np.c_[np.ones([np.size(a2, 0), 1]), a2]
        z3 = np.dot(Theta2, a2.T)
        a3 = sigmoid(z3).T

        for i in range(m):
            prediction[i] = np.argmax(a3[i, :])
        return prediction

    def randInitializeWeights(length_in, length_out, epsilon_init = 0.12):
        weights = np.zeros([length_out, length_in + 1])
        weights = np.random.rand(length_out, length_in + 1) * 2 * epsilon_init - epsilon_init
        return weights

    def cost(nn_parameters, input_layer_size, hidden_layer_size, X, y, number_of_labels, lambdaRegulator = 0):
        Theta1 = nn_parameters[:hidden_layer_size * (input_layer_size + 1)].reshape(hidden_layer_size, input_layer_size+1)
        Theta2 = nn_parameters[hidden_layer_size * (input_layer_size + 1):].reshape(number_of_labels, hidden_layer_size+1)

        m = np.size(X, 0)
        X = np.c_[np.ones([m, 1]), X]
        I = np.eye(number_of_labels)
        Y = np.zeros([m, number_of_labels])
        for i in range(m):
            Y[i, :] =  I[int(y[i]), :]

        z2 = np.dot(Theta1, X.T)
        a2 = sigmoid(z2).T
        a2 = np.c_[np.ones([np.size(a2, 0), 1]), a2]
        z3 = np.dot(Theta2, a2.T)
        h = sigmoid(z3).T

        J = -Y * np.log(h) - (1-Y) * np.log(1-h)
        J = (1/m) * np.sum(J)
        regulationTerm = np.sum(Theta1[:, 1:]**2) + np.sum(Theta2[:, 1:]**2)
        regulationTerm *= (lambdaRegulator/(2*m))
        J = J + regulationTerm
        return J

    def gradient(nn_parameters, input_layer_size, hidden_layer_size, X, y, number_of_labels, lambdaRegulator = 0):
        Theta1 = nn_parameters[:hidden_layer_size * (input_layer_size + 1)].reshape(hidden_layer_size, input_layer_size+1)
        Theta2 = nn_parameters[hidden_layer_size * (input_layer_size + 1):].reshape(number_of_labels, hidden_layer_size+1)

        m = np.size(X, 0)
        X = np.c_[np.ones([m, 1]), X]
        I = np.eye(number_of_labels)
        Y = np.zeros([m, number_of_labels])
        for i in range(m):
            Y[i, :] =  I[int(y[i]), :]

        z2 = np.dot(Theta1, X.T)
        a2 = sigmoid(z2).T
        a2 = np.c_[np.ones([np.size(a2, 0), 1]), a2]
        z3 = np.dot(Theta2, a2.T)
        h = sigmoid(z3).T

        sigma3 = h - Y
        z2 = z2.T
        z2 = np.c_[np.ones([np.size(z2, 0), 1]), z2]
        sigma2 = np.dot(sigma3, Theta2) * neuralNetwork.sigmoid_derivative(z2)
        sigma2 = sigma2[:, 1:]

        delta1 = np.dot(sigma2.T, X)
        delta2 = np.dot(sigma3.T, a2)

        Theta1[:, 0] = 0
        Theta2[:, 0] = 0

        Theta1_gradient = (1/m)*delta1.T + (lambdaRegulator/m)*Theta1.T
        Theta2_gradient = (1/m)*delta2.T + (lambdaRegulator/m)*Theta2.T

        gradient = np.zeros(np.size(Theta1_gradient) + np.size(Theta2_gradient))
        gradient[:np.size(Theta1_gradient)] = Theta1_gradient.flatten()
        gradient[np.size(Theta1_gradient):] = Theta2_gradient.flatten()

        return gradient

    def ReLU(x): # Rectified linear unit
        return np.maximum(0, x)

    def ReLu_derivative(x):
        x[x<=0] = 0
        x[x>0] = 1
        return x
