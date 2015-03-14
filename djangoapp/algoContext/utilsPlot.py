__author__ = 'jiusi'

import os
import librosa
import numpy as np
import matplotlib.pyplot as plt

import utilsData as ud
import parameters as param

from sklearn import mixture
from librosa.feature import mfcc
from librosa.core import resample
from librosa.display import specshow

from utils import utils


def plotMFCCs(filePathList):
    rates = []
    sigs = []
    for filePath in filePathList:
        rate, sig = ud.getDataFromPath(filePath)
        rates.append(rate)
        sigs.append(sig)

    mfccValueList = []
    mfccDeltaList = []
    for rate, sig in zip(rates, sigs):
        mfccValue = mfcc(y=sig, sr=rate, n_mfcc=param.N_MFCC)
        mfccDelta = librosa.feature.delta(mfccValue)
        mfccValueList.append(mfccValue)
        mfccDeltaList.append(mfccDelta)

    unitHeight = 10
    figHeight = 10 * (len(filePathList) * 2)
    figSize = (figHeight, unitHeight)
    print figSize

    plt.figure(figsize=figSize)

    for i, tu in enumerate(zip(mfccValueList, mfccDeltaList)):
        mfccValue = tu[0]
        mfccDelta = tu[1]

        fileName = utils.path_leaf(filePathList[i])

        a = len(filePathList) * 2
        b = 1
        c = i * 2 + 1
        print a, b, c
        plt.subplot(a, b, c)
        librosa.display.specshow(mfccValue)
        plt.ylabel('mfcc:' + fileName)
        plt.colorbar()

        print a, b, c+1
        plt.subplot(a, b, c+1)
        librosa.display.specshow(mfccDelta)
        plt.ylabel('mfcc delta')
        plt.colorbar()

    plt.tight_layout()
    plt.show()

# quite_smarti = '/Users/jiusi/Desktop/smarti_ref.wav'
# quite_iphone = '/Users/jiusi/Desktop/iphone_ref.m4a'
#
# plotMFCCs([quite_smarti, quite_iphone])

def plotMFCCDiff(rate1, sig1, rate2, sig2):

    highSig, lowSig = sig1, sig2
    highRate, lowRate = rate1, rate2
    if rate2 > rate1:
        highSig = sig2
        lowSig = sig1
        highRate = rate2
        lowRate = rate1

    rehi = resample(highSig, highRate, lowRate)

    mfcc1 = mfcc(rehi, lowRate, n_mfcc=param.N_MFCC)
    mfcc2 = mfcc(lowSig, lowRate, n_mfcc=param.N_MFCC)

    l, s = mfcc1, mfcc2
    if mfcc2.shape[1] > mfcc1.shape[1]:
        l, s = mfcc2, mfcc1
    rel = l[:, :s.shape[1]]

    errors = []
    for i in range(0, 100):
        s1 = s[:, i:]
        s2 = rel[:, :rel.shape[1]-i]

        print 's1.shape:', s1.shape, 's2.shape:', s2.shape, 's1.avg:', np.average(s1)

        errors.append(np.sum(np.abs(s1, s2) **2) *.5)

    print 'max error:', np.max(errors)
    print 'min error:', np.min(errors)
