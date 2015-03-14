__author__ = 'jiusi'
from sklearn.externals import joblib
import ntpath
import os
import parameters as param
import uuid
import yaml
import numpy as np
import scipy.io.wavfile as wavfile

def loadClassifier(clfPath):
    clf = joblib.load(clfPath)
    print 'classifier recovered from:', clfPath
    return clf

def saveClassifier(clf, savePath):
    dirName = os.path.dirname(savePath)
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print 'savePath:', savePath, 'don not exist, os make dir called'

    s = joblib.dump(clf, savePath)
    print 'classifier saved at:', s

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def saveUploadedFile(f, savePath):
    dirName = os.path.dirname(savePath)
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print 'savePath:', savePath, 'don not exist, os make dir called'

    dest = open(savePath, 'wb+')
    for chunk in f.chunks():
        dest.write(chunk)
    dest.close()

    print 'uploaded file save to:', savePath

def loadMotionClfs():
    moClfVH = loadClassifier(param.moClf_VH)
    moClfSS_L1 = loadClassifier(param.moClf_SS_L1)
    moClfSS_L2A = loadClassifier(param.moClf_SS_L2A)
    moClfSS_L2I = loadClassifier(param.moClf_SS_L2I)

    return moClfVH, moClfSS_L1, moClfSS_L2A, moClfSS_L2I

def loadContextClfs():
    ctxClfProd = loadClassifier(param.ctxClf_PROD)
    return ctxClfProd

def loadEventClfs():
    evnClfProd = loadClassifier(param.evnClf_PROD)
    return evnClfProd

def getCorrectRate(trueTags, pred):
    count = 0
    for trueTag, p in zip(trueTags, pred):
        if trueTag == p:
            count += 1
    return count / len(trueTags)

def genContextClfDir(clfType):
    return param.contextClfPrefix + '_' + clfType + '_' + str(uuid.uuid4()) + '/'

def genMotionClfDir(clfType):
    return param.motionClfPrefix + '_' + clfType + '_' + str(uuid.uuid4()) + '/'

def genContextParamFileName():
    return param.contextParamPrefix + '_' + str(uuid.uuid4()) + '.json'

def genMotionParamFileName():
    return param.motionParamPrefix + '_' + str(uuid.uuid4()) + '.json'

def genSoundFileName():
    return param.soundClipPrefix + '_' + str(uuid.uuid4()) + '.mp3'

def getFeatureParam4Ctx():
    fp = {}
    fp['N_MFCC'] = param.N_MFCC
    fp['FREQ_MAX'] = param.FREQ_MAX
    fp['CTX_FRAME_IN_SEC'] = param.CTX_FRAME_IN_SEC
    fp['EVN_FRAME_IN_SEC'] = param.EVN_FRAME_IN_SEC
    fp['FEATURES'] = param.FEATURES

    return fp

def getFeatureParam4Evt():
    fp = {}
    fp['N_MFCC'] = param.N_MFCC
    fp['FREQ_MAX'] = param.FREQ_MAX
    fp['FRAME_IN_SEC'] = param.EVN_FRAME_IN_SEC
    fp['FEATURES'] = param.FEATURES

    return fp

def getTrainParam4Ctx(paramSavePath):
    jsonData = open(paramSavePath)
    trainParam = yaml.load(jsonData)
    trainParam['FRAME_IN_SEC'] = trainParam['CTX_FRAME_IN_SEC']
    return trainParam

def getTrainParam4Evn(paramSavePath):
    jsonData = open(paramSavePath)
    trainParam = yaml.load(jsonData)
    trainParam['FRAME_IN_SEC'] = trainParam['EVN_FRAME_IN_SEC']
    return trainParam

def writeWavfile(rate, data, savePath):
    data = np.asarray(data, dtype=np.int16)
    wavfile.write(savePath, rate, data)