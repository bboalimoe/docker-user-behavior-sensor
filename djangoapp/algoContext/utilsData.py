__author__ = 'jiusi'

import os

import parameters as param
import numpy as np

import audioDBReader
import scipy.io.wavfile as wave

from pydub import AudioSegment

from librosa.feature import mfcc
from librosa.core import resample


def getClipSig(start, stop, rate, fileSig):
    startIdx = start * rate
    stopIdx = stop * rate

    clip = fileSig[startIdx: stopIdx+1]
    return clip.tolist()

def getEventSigFromFile(rate, fileSig, fileEvents):

    eventGroupedSig = {}
    clipMarks = []
    for event in fileEvents:
        eventName = event['type']
        start = event['start']
        stop = event['stop']

        clipMarks.append([start, stop])

        clipSig = getClipSig(start, stop, rate, fileSig)

        if not eventName in eventGroupedSig:
            eventGroupedSig[eventName] = []
        eventGroupedSig[eventName].extend(clipSig)

    # categorize remaining into Unknown
    eventGroupedSig[param.EVN_UNKNOWN] = []
    lastMark = 0
    for mark in clipMarks:
        start = mark[0]
        stop = mark[1]
        clipSig = getClipSig(lastMark, start, rate, fileSig)
        eventGroupedSig[param.EVN_UNKNOWN].extend(clipSig)
        lastMark = stop

    return eventGroupedSig


def getEventGroupedSig(fileDict, trainDataSetDict):
    fileNames = [fileName for fileName in trainDataSetDict]
    eventGroupedDict = {}
    for fileName in fileNames:

        filePath = param.audioRoot + fileDict[fileName]['fileNameLeft']
        rate, sig = getDataFromPath(filePath)

        events = fileDict[fileName]['events']

        temp = getEventSigFromFile(rate, sig, events)

        for eventName in temp:
            if eventName not in eventGroupedDict:
                eventGroupedDict[eventName] = []
            eventGroupedDict[eventName].extend(temp[eventName])

    eventGrouped = []
    eventGroupedL3 = []

    for eventName in eventGroupedDict:
        eventGrouped.append(eventGroupedDict[eventName])

        eventId = getL3Id(eventName)
        eventGroupedL3.append(eventId)

    return rate, eventGrouped, eventGroupedL3


def getFileGroupedSig(fileDict, trainDataSetDict):
    fileGroupedSig = []
    fileGroupedL2 = []
    rate = 0

    fileNames = [name for name in trainDataSetDict]

    print "total train files:", len(fileNames)

    for name in fileNames:
        filePath = param.audioRoot + fileDict[name]['fileNameLeft']

        rate, sig = getDataFromPath(filePath)

        fileGroupedSig.append(sig)
        L2Code = trainDataSetDict[name]['L2']
        fileGroupedL2.append(L2Code)

    return rate, fileGroupedSig, fileGroupedL2




def getData4Ctx(trainParam):
    classDict, fileDict = audioDBReader.readJson(param.audioDbJsonPath)
    print "total data base files:", len(fileDict)

    trainDataSetDict = trainParam['fileContextMap']

    return getFileGroupedSig(fileDict, trainDataSetDict)

def getData4Evn(trainParam):
    classDict, fileDict = audioDBReader.readJson(param.audioDbJsonPath)

    trainDataSetDict = trainParam['fileContextMap']
    return getEventGroupedSig(fileDict, trainDataSetDict)



def sigToFrames(rate, sig, frameTime):

    sig = np.array(sig)

    frameSize = rate * frameTime
    if len(sig) < frameSize:
        print 'warning! input signal smaller than a frame'
        return [sig]

    trimmed = sig[0:(len(sig) - len(sig) % frameSize)]
    trimmed = np.array(trimmed)

    frames = trimmed.reshape(len(trimmed) / frameSize, frameSize)



    return frames


def printAudioParams(audioPath, format):
    a = AudioSegment.from_file(audioPath, format)
    print a

def getDataFromPath(filePath):
    fileName, extension = os.path.splitext(filePath)
    print 'name:', fileName, ' ext:', extension

    if extension.lower() == '.mp3':
        wavPath = fileName + '.wav'
        mp3 = AudioSegment.from_mp3(filePath)
        mp3.export(wavPath, format='wav')
        filePath = wavPath
    elif extension.lower() == '.m4a':
        wavPath = fileName + '.wav'
        m4a = AudioSegment.from_file(filePath, 'm4a')
        m4a.export(wavPath, format='wav')
        filePath = wavPath

    print filePath
    rate, sig = wave.read(filePath)
    return rate, sig

def getL1Text(l2code):
    l1code = param.L2L1Map[str(l2code)]
    return param.L1ContextIdNameMap[l1code]

def getL1Code(l2code):
    return param.L2L1Map[str(l2code)]

def getL2Text(pred):
    return param.L2ContextIdNameMap[str(pred)]

def getL3Id(text):
    for id in param.L3EventIdNameMap:
        if param.L3EventIdNameMap[id] == text:
            return int(id)
    return 0

def getL3Texts(ids):
    texts = []
    for id in ids:
        texts.append(param.L3EventIdNameMap[str(id)])
    return texts
