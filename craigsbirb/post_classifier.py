from numpy import linalg
import numpy as np
import json
import time
from feature_extractor import Feature_Extractor
import os
import random
from matplotlib import pyplot as plt
import pandas as pd
from sklearn import svm
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from sklearn import metrics

file_dir = os.path.dirname(os.path.realpath(__file__))
SVM_FILE = os.path.join(file_dir, 'w_svm.p')
FE_FILE = os.path.join(file_dir, 'fe_df.csv')
RANDOM_STATE = 42
THRESHOLD = 4

def linear_kernel(x1, x2):
    return np.dot(x1, x2)


def polynomial_kernel(x, y, p=3):
    return (1 + np.dot(x, y)) ** p


def gaussian_kernel(x, y, sigma=5.0):
    return np.exp(-linalg.norm(x-y)**2 / (2 * (sigma ** 2)))


class Post_Classifier:
    def __init__(self, threshold=4):
        print("you've made a classifier")
        self.threshold=4

    def train(self):
        pass

    def predict(self, df):
        pass


if __name__ == "__main__":
    here = os.path.dirname(os.path.realpath(__file__))
    jf = os.path.join(here, 'training_data', 'training.json')
    with open(jf, 'r') as f:
        d = json.load(f)

    d2 = dict()
    d2['links'] = [k for k in d]
    d2['scores'] = [v for k, v in d.items()]
    count_dict = {val: len([x for x in d2['scores'] if x == val]) for
                  val in range(1, 6)}
    print(count_dict)

    if not os.path.isfile(FE_FILE):
        fe = Feature_Extractor()
        df_original = fe.process_posts(json_fname='updated_posts.json')
        df_original.to_csv(FE_FILE)
    else:
        df_original = pd.read_csv(FE_FILE)

    print(df_original.columns)
    df = df_original.copy()
    y = np.array(df_original.score).astype(float)
    for idx in range(len(y)):
        if y[idx] >= THRESHOLD:
            y[idx] = 1
        else:
            y[idx] = 0

    non_numeric_cols = ['title']
    df.drop(non_numeric_cols, 1, inplace=True)
    X = np.array(df.drop(['score'], 1)).astype(float)
    X = scale(X, axis=0)
    print(X.size)
    acc_list = []
    for x in range(200):
        RANDOM_STATE = random.randint(1, 1000)
        X_train, X_test, y_train, y_test = train_test_split(X,
                                                            y,
                                                            test_size=0.25,
                                                            random_state=RANDOM_STATE)
        # fit the model and get the separating hyperplane using weighted classes
        #usr_input = input('Use existing model?\n[y]>>')
        if True:  # ('n' in usr_input) or (not os.path.isfile(
            # SVM_FILE)):
            wclf = svm.SVC(kernel='rbf', class_weight={1: 20})
            #print("Training the svm")
            start = time.time()
            wclf.fit(X_train, y_train)
            end = time.time()
            #print("Finished training! ({} seconds)".format(end -
            # start))
            with open(SVM_FILE, 'wb') as f:
                pickle.dump(wclf, f)
        else:
            with open(SVM_FILE, 'rb') as f:
                wclf = pickle.load(f)

        pred_test = wclf.predict(X_test)

        # Show prediction accuracies in scaled and unscaled data.
        acc_list.append(metrics.accuracy_score(y_test, pred_test))
        #print('\nPrediction accuracy for RANDOM_STATE = {
        # }'.RANDOM_STATE)
        #print('{:.2%}\n'.format())

    for idx, x in enumerate(acc_list):
        print("{}: {:.2%}".format(idx, x))

    print(''.join(['+']*60))
    print('Average Performance: {:.2%}'.format(sum(acc_list)/len(
        acc_list)))
    print(''.join(['+']*60))
