__author__ = 'jiusi'

import math
import utilsData as ud
import numpy as np
from scipy.signal import lfilter, firwin

WINDOW = 1/2.0 #sec
JITTER_DIST = 1/5.0 #sec
THRES = 5

STEP_MIN_GAP = 0.6 #sec
STEP_MAX_GAP = 1.5 #sec


def peakDetection(sig, sampleFreq):
    windowN = math.ceil(sampleFreq * WINDOW)

    print "windowN:", windowN

    peakList = []

    for i in range(1, len(sig)-1):
        searchStart = i - windowN/2
        searchEnd = i + windowN/2 + 1
        if searchStart < 0:
            searchStart = 0
        if searchEnd > len(sig):
            searchEnd = len(sig) - 1

        leftMin = min(sig[searchStart: i])
        rightMin = min(sig[i:searchEnd])

        if sig[i] > sig[i-1] and sig[i] > sig[i+1]:

            leftRate = (sig[i] - leftMin) / (WINDOW/2)
            rightRate = (sig[i] - rightMin) / (WINDOW/2)

            if leftRate > THRES and rightRate > THRES:
                peakList.append(i)

    return peakList

def jitterPeakFilter(sig, peakIdx, sampleFreq):
    jitterWindow = JITTER_DIST * sampleFreq
    print 'jitterWindow:', jitterWindow

    if jitterWindow < 1:
        jitterWindow = 1
    jitterWindow = math.ceil(jitterWindow)

    perged = []
    for i in range(1, len(peakIdx)):
        if peakIdx[i] - peakIdx[i-1] < jitterWindow:
            continue
        else:
            perged.append(peakIdx[i])

    return perged

def stepFilter(sig, peakIdx, sampleFreq):
    stepMinGap = STEP_MIN_GAP*sampleFreq
    stepMaxGap = STEP_MAX_GAP*sampleFreq
    print 'stepMin, Max:', stepMinGap, stepMaxGap

    perged = []
    for i in range(1, len(peakIdx)):
        if peakIdx[i] - peakIdx[i-1] <= stepMaxGap and peakIdx[i] - peakIdx[i-1] >= stepMinGap:
            perged.append(peakIdx[i])

    return perged


def stepDetect(rawData):

    accData = ud.getDataBySensorType('accelerometer', rawData)

    duration = ud.getDuration(accData)
    sampleFreq = ud.getAccSampleFreq(accData)

    nyq_rate = sampleFreq / 2.
    # The cutoff frequency of the filter: 3Hz
    cutoff_hz = 3
    # Length of the filter (number of coefficients, i.e. the filter order + 1)
    numtaps = 2

    mergeList = []
    for data in accData:
        acc = data['values']
        sqrSum = np.sqrt(np.dot(acc, acc))
        mergeList.append([sqrSum])

    mergeList = np.array(mergeList)

    if cutoff_hz < nyq_rate:
        fir_coeff = firwin(numtaps, cutoff_hz/nyq_rate)
        filtered_sig = lfilter(fir_coeff, 1.0, mergeList)
    else:
        filtered_sig = mergeList

    peakList = peakDetection(filtered_sig, sampleFreq)
    peakList = np.array(peakList)
    peakList = jitterPeakFilter(filtered_sig, peakList, sampleFreq)
    stepList = stepFilter(filtered_sig, peakList, sampleFreq)

    minSteps = duration * STEP_MAX_GAP
    maxSteps = duration * STEP_MIN_GAP

    if stepList >= minSteps and stepList <= maxSteps:
        return True
    else:
        return False
