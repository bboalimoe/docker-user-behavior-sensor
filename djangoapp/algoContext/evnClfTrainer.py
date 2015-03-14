__author__ = 'jiusi'


import numpy as np

from sklearn import mixture
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from sklearn.svm import SVC

from sklearn import cross_validation

import parameters as param
import featureGenerator as fg

from utils import utils


def trainTestClfs(rate, eventGroupedSig, eventGroupedY, trainParam, clfSavePath):

    X, y = fg.getXy(rate, eventGroupedSig, eventGroupedY, trainParam)

    print 'context feature retrieved'

    knn = KNeighborsClassifier()
    gmm = mixture.GMM(n_components=trainParam['N_COMPONENTS'])
    svm = SVC(kernel=str(trainParam['SVM_KERNEL']), C=trainParam['SVM_C'])


    if trainParam['CLF'] == 'KNN':
        knn.fit(X, y)
        utils.saveClassifier(knn, clfSavePath)
        print 'KNN clf training finished, saved at:', clfSavePath

        cScore = cross_validation.cross_val_score(knn, X=X, y=y, cv=trainParam['K_FOLD'])
        print 'KNN with feature schema', trainParam['FEATURE_SCHEMA'], cScore

        return cScore

    if trainParam['CLF'] == 'SVM':
        svm.fit(X, y)
        utils.saveClassifier(svm, clfSavePath)
        print 'SVM clf training finished, saved at:', clfSavePath

        cScore = cross_validation.cross_val_score(svm, X=X, y=y, cv=trainParam['K_FOLD'])
        print 'SVM with feature schema:', trainParam['FEATURE_SCHEMA'], cScore

        return cScore

    if trainParam['CLF'] == 'GMM':
        gmm.fit(X)
        utils.saveClassifier(gmm, clfSavePath)
        print 'GMM clf training finished, saved at:', clfSavePath

        return 0
