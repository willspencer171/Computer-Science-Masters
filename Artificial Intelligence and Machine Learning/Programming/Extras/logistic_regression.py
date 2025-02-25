"""Logistic regression is a linear regression model that
is used for classification of instances

The formulae involved are a little complex, and, unlike the
least squares method, finding parameters for the linear model
relies on maximising the log-likelihood"""
import numpy as np
from scipy.optimize import minimize
from sklearn.datasets import make_classification
from sklearn.metrics import confusion_matrix, precision_score, recall_score


# Probability values are given by the logit function
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# We use minimisation of the negative log-likelihood to compute maximisation
def neg_log_likelihood(theta, X, y, lambda_=1):
    p = sigmoid(X @ theta)
    likelihood = y * np.log(p) + (1 - y) * np.log(1 - p)
    regularisation = (lambda_ / 2) * np.sum(theta[1:] ** 2)
    return -np.sum(likelihood) + regularisation

# Gradient of the log-likelihood
def gradient(theta, X, y, lambda_=1):
    p = sigmoid(X @ theta)
    grad = X.T @ (p - y)
    grad[1:] += lambda_ * theta[1:]
    return grad

def maximise_log_likelihood(X, y, lambda_=1):
    # Initialize theta (parameters)
    theta_init = np.zeros(X.shape[1])

    # Optimize using L-BFGS
    result = minimize(fun=neg_log_likelihood, x0=theta_init, args=(X, y, lambda_), 
                    jac=gradient, method="L-BFGS-B")

    # Optimal parameters
    return result.x

def compute_response_preds(X, y, lambda_=1):
    # True or false statement of classification
    theta_opt = maximise_log_likelihood(X, y, lambda_)
    return sigmoid(X @ theta_opt) >= 0.5

def compute_accuracy(y, y_pred):
    # Accuracy is the average of the correct predictions
    return np.mean(y_pred == y)



def compute_confusion_matrix(y, y_pred):
    return confusion_matrix(y, y_pred)

def compute_performance_metrics(y, y_pred):
    accuracy = compute_accuracy(y, y_pred)
    precision = precision_score(y, y_pred)
    recall = recall_score(y, y_preds)

    return (accuracy, precision, recall)

X, y = make_classification(n_samples=1000)
X = np.c_[np.ones(X.shape[0]), X]

y_preds = compute_response_preds(X, y, 5)

accuracy, precision, recall = compute_performance_metrics(y, y_preds)

print(f'Accuracy: {accuracy:.2f}\nPrecision: {precision:.2f}\nRecall: {recall:.2f}')
