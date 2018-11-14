import sklearn as skl
from numpy import linalg
import numpy as np


def linear_kernel(x1, x2):
    return np.dot(x1, x2)


def polynomial_kernel(x, y, p=3):
    return (1 + np.dot(x, y)) ** p


def gaussian_kernel(x, y, sigma=5.0):
    return np.exp(-linalg.norm(x-y)**2 / (2 * (sigma ** 2)))


class Post_Classifier:
    def __init__(self):
        print("you've made a classifier")

    def train(self):
        pass

    def predict(self, df):
        pass
