import json
import numpy as np
import pprint

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


FNAME = "./data/0.json"
KSPLITS = 4
RANDOM = 42

def train_and_test_models(X_tr, y_tr, X_test, y_test):
    pp = pprint.PrettyPrinter(indent=4)
    names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Gaussian Process",
             "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
             "Naive Bayes", "QDA"]

    clf_d = dict()
    for n in names:
        clf_d[n] = []

    clf_d_test = clf_d.copy()

    classifiers = [
        KNeighborsClassifier(3),
        SVC(kernel="linear", C=0.025),
        SVC(gamma=2, C=1),
        GaussianProcessClassifier(1.0 * RBF(1.0)),
        DecisionTreeClassifier(max_depth=8),
        RandomForestClassifier(max_depth=8, n_estimators=10, max_features=1),
        MLPClassifier(alpha=1, max_iter=1000),
        AdaBoostClassifier(),
        GaussianNB(),
        QuadraticDiscriminantAnalysis()]

    # Iterate over classifiers with KFold
    kf = StratifiedKFold(n_splits=KSPLITS)
    for train_index, test_index in kf.split(X_train, y_train):
        X_train_k, X_test_k = X_tr[train_index], X_tr[test_index]
        y_train_k, y_test_k = y_tr[train_index], y_tr[test_index]
        for i, (name, clf) in enumerate(zip(names, classifiers)):
            aux = clf.fit(X_train_k, y_train_k.flatten())
            classifiers[i] = aux
            score = clf.score(X_test_k, y_test_k)
            clf_d[name].append(score)

    max, max_i = 0, 0
    for i, n in enumerate(clf_d):
        val = clf_d[n]
        clf_d[n] = sum(val) / len(val)
        if clf_d[n] > max:
            max, max_i = clf_d[n], i

    print("Training accuracies")
    pp.pprint(clf_d)
    # model = classifiers[max_i]

    for name, clf in zip(names, classifiers):
        clf_d_test[name] = clf.score(X_test, y_test)

    print("Testing accuracies")
    pp.pprint(clf_d_test)

if __name__ == '__main__':
    with open(FNAME) as json_file:
        data = json.load(json_file)

    np_data = np.array(data)
    X = np.vstack(np_data[..., 0])
    y = np.vstack(np_data[..., 1])


    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=0.3, random_state=RANDOM)

    train_and_test_models(X_train, y_train, X_test, y_test)







######################################
# import matplotlib.pyplot as plt
# from sklearn.manifold import TSNE
# from sklearn.decomposition import PCA
# X_TSNE = TSNE(n_components=2).fit_transform(np_data)
# X_PCA = PCA(n_components=2).fit_transform(np_data)
#
# plt.title("PCA and TSNE data into 2 dimensions")
# plt.scatter(X_TSNE[:,0], X_TSNE[:,1], s=5, label="TSNE")
# plt.scatter(X_PCA[:,0], X_PCA[:,1], s=5, label="PCA")
# plt.legend()
# plt.show()
