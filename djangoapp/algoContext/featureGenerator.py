__author__ = 'jiusi'


from librosa.feature import mfcc as mfccAlgo
from librosa.feature import delta as mfccDelta

import utilsData as ud

import numpy as np

# NOTE! librosa treat vector list differently than NDArray
# The MFCC passed to function is in NDArray's convention
# Need to transpose it before passing to librosa functions

def sigToMFCC(rate, sig, freqMax, n_mfcc):
    return mfccAlgo(y=sig, sr=rate, n_mfcc=n_mfcc, fmax=freqMax).T

def mfccToMFCCDelta(mfccVectorList, order=1):
    mfccVectorList = mfccVectorList.T
    return mfccDelta(mfccVectorList, order=order).T

def getXy(rate, fileGroupedSig, fileGroupedY, featureParam):

    frameTime = featureParam['FRAME_IN_SEC']
    freqMax = featureParam['FREQ_MAX']
    nMfcc = featureParam['N_MFCC']

    X = []
    y = []
    for i, fileSig in enumerate(fileGroupedSig):
        frames = ud.sigToFrames(rate, fileSig, frameTime)
        for frame in frames:
            tag = fileGroupedY[i]
            mfcc = sigToMFCC(rate, frame, freqMax, nMfcc)
            feature = np.array(mfcc)

            if 'mfccDelta' in featureParam['FEATURES']:
                mfccDelta = mfccToMFCCDelta(feature)
                feature = np.append(feature, mfccDelta, axis=1)
            if 'mfccDelta2' in featureParam['FEATURES']:
                mfccDelta2 = mfccToMFCCDelta(mfcc, order=2)
                feature = np.append(feature, mfccDelta2, axis=1)

            X.extend(feature)
            y.extend([tag for j in range(0, feature.shape[0])])

    return X, y

def getX(rate, sig, featureParam):
    frameTime = featureParam['FRAME_IN_SEC']
    freqMax = featureParam['FREQ_MAX']
    nMfcc = featureParam['N_MFCC']

    X = []
    frames = ud.sigToFrames(rate, sig, frameTime)
    print 'len(frames):', len(frames)
    for frame in frames:
        mfcc = sigToMFCC(rate, frame, freqMax, nMfcc)
        feature = np.array(mfcc)

        if 'mfccDelta' in featureParam['FEATURES']:
            mfccDelta = mfccToMFCCDelta(feature)
            feature = np.append(feature, mfccDelta, axis=1)
        if 'mfccDelta2' in featureParam['FEATURES']:
            mfccDelta2 = mfccToMFCCDelta(mfcc, order=2)
            feature = np.append(feature, mfccDelta2, axis=1)

        X.extend(feature)
    print 'feature list length:', len(X)
    return X

def getFeatureFrameSize(rate, frameTime, freqMax, n_mfcc):
    testFrame = np.zeros(rate * frameTime)
    mfcc = sigToMFCC(rate, testFrame, freqMax, n_mfcc)
    return mfcc.shape[0]
