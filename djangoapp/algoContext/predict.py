__author__ = 'jiusi'

import numpy as np

import utilsData as ud
import featureGenerator as fg


def predictMp3(mp3File, clfCtx, clfEvn, featureParam):
    rate, sig = ud.getDataFromPath(mp3File)
    ctxPrediction  = predContextBySig(rate, sig, clfCtx, featureParam)
    evnPredictions = predEventBySig(rate, sig, clfEvn, featureParam)
    # evnPredictions = []
    return ctxPrediction, evnPredictions


def predContextBySig(rate, sig, clf, featureParam):
    featureParam['FRAME_IN_SEC'] = featureParam['CTX_FRAME_IN_SEC']
    X = fg.getX(rate, sig, featureParam)

    npX = np.array(X)
    print 'npX.shape:', npX.shape

    rawPrediction = clf.predict(X)
    return refinePrediction(rawPrediction)

def predEventBySig(rate, sig, clf, featureParam):
    featureParam['FRAME_IN_SEC'] = featureParam['EVN_FRAME_IN_SEC']
    X = fg.getX(rate, sig, featureParam)

    npX = np.array(X)
    print 'npX.shape:', npX.shape

    rawPrediction = clf.predict(X)
    if isinstance(rawPrediction, np.ndarray):
        rawPrediction = rawPrediction.tolist()
    return rawPrediction


def refinePrediction(rawPrediction):
    classMap = {}
    for p in rawPrediction:
        if p in classMap:
            classMap[p] += 1
        else:
            classMap[p] = 1

    maxProbClass = max(classMap, key=lambda i: classMap[i])
    return maxProbClass



#
# def refinePrediction(predictionList, frameSize):
#
#     predictionList = np.array(predictionList)
#     frameGrouped = predictionList.reshape(predictionList.size/frameSize, frameSize)
#     merged = []
#     for predictionCluster in frameGrouped:
#         classMap = {}
#         for p in predictionCluster:
#             if p in classMap:
#                 classMap[p] += 1
#             else:
#                 classMap[p] = 1
#
#         maxProbabilityClass = max(classMap, key=lambda i: classMap[i])
#         merged.append(maxProbabilityClass)
#     return merged
