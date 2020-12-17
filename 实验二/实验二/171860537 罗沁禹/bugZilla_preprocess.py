import pandas
from sklearn.preprocessing import OrdinalEncoder
import numpy as np
from sklearn.model_selection import KFold
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
def remove_column():
    data = pandas.read_csv("bugSample.csv")
    i = 0
    for k,importance in enumerate(data["importance"]):
        i += 1
        value = importance.split()
        #if 2 < len(value):
            #data.loc[k, "importance"] = value[0] + " "+ value[1]
        data.loc[k, "importance"] = value[1]

        print(data["importance"][k])
        print(i)
    data.to_csv("bugSample_processed_2.csv", index=False)


def encode():
    data = pandas.read_csv("bugSample_processed_2.csv")
    enc = OrdinalEncoder()

    data = enc.fit_transform(data.values)
    data = pandas.DataFrame(data, columns=['status','product','component','hardware','importance'])
    data.to_csv("bugSample_encoded.csv", index = False)


def train_NB():
    data = pandas.read_csv("bugSample_encoded.csv").values
    #data = pandas.read_csv("test.csv").values
    X = np.array(data[:, 0:-1])
    y = np.array(data[:, -1])
    kf = KFold(n_splits=5)
    clf = GaussianNB()
    print(clf)
    acc = 0
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf.partial_fit(X_train, y_train, classes=[0, 1, 2, 3, 4, 5, 6])
        predict = clf.predict(X_test)
        acc = accuracy_score(y_test, predict)
    print("Naive Bayes: ", acc)


def train_deciTree() :
    data = pandas.read_csv("bugSample_encoded.csv").values
    X = np.array(data[:, 0:-1])
    y = np.array(data[:, -1])
    kf = KFold(n_splits=5)
    clf = DecisionTreeClassifier()
    print(clf)

    acc = 0
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        predict = clf.predict(X_test)
        acc = accuracy_score(y_test, predict)
    print("Decision Tree: ", acc)

def train_random_forest():
    data = pandas.read_csv("bugSample_encoded.csv").values
    X = np.array(data[:, 0:-1])
    y = np.array(data[:, -1])
    kf = KFold(n_splits=5)
    clf = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=0)
    print(clf)
    acc = 0
    for train_index, test_index in kf.split(X):

        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        predict = clf.predict(X_test)
        acc = accuracy_score(y_test, predict)
    print("Random Forest: ", acc)

def train_MLP():
    data = pandas.read_csv("bugSample_encoded.csv").values
    X = np.array(data[:, 0:-1])
    y = np.array(data[:, -1])
    kf = KFold(n_splits=5)
    clf = MLPClassifier(hidden_layer_sizes=100, alpha=0.0001)
    print(clf)

    acc = 0
    for train_index, test_index in kf.split(X):

        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        predict = clf.predict(X_test)
        acc = accuracy_score(y_test, predict)
    print("MLP: ", acc)


def train_SVM():
    data = pandas.read_csv("bugSample_encoded.csv").values
    X = np.array(data[:, 0:-1])
    y = np.array(data[:, -1])
    kf = KFold(n_splits=5)
    clf = SVC(gamma='auto')
    print(clf)

    acc = 0
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        predict = clf.predict(X_test)
        acc = accuracy_score(y_test, predict)
    print("SVM: ", acc)
train_NB()
train_deciTree()
train_random_forest()
train_MLP()
train_SVM()
