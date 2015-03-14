__author__ = 'jiusi'

import parameters as param
from mixpanel import Mixpanel
mp = Mixpanel(param.MIX_PANEL_TOKEN)

import utils

def logFeaturePrediction(distinct_id, name, reqBody, prediction):
    logProperties = {}

    logProperties['X'] = reqBody['X']
    logProperties['prediction'] = prediction.tolist()
    if 'y' in reqBody:
        logProperties['y'] = reqBody['y']
        rate = utils.getCorrectRate(reqBody['y'], prediction)
        logProperties['correct_rate'] = rate

    try:
        mp.track(distinct_id, name, logProperties)
    except Exception, e:
        print 'logFeaturePrediction failed'
        print e

def logMotionPrediction(distinct_id, name, rawData, X, result, y=None):
    logProperties = {}

    logProperties['rawData'] = rawData
    logProperties['X'] = X

    if 'predVH' in result:
        logProperties['predVH'] = result['predVH']
    if 'predSS' in result:
        logProperties['predSS'] = result['predSS']

    if y:
        logProperties['y'] = y
        if 'predVH' in result:
            rateVH = utils.getCorrectRate(y, result['predVH'])
            logProperties['correct_rate_VH'] = rateVH
        if 'predSS' in result:
            rateSS = utils.getCorrectRate(y, result['predSS'])
            logProperties['correct_rate_SS'] = rateSS

    try:
        mp.track(distinct_id, name, logProperties)
    except Exception, e:
        print 'logMotionPrediction failed'
        print e

def logContextPrediction(distinct_id, name, soundSavePath, ctxPred, evnPreds):
    logProperties = {}

    logProperties['soundSavePath'] = soundSavePath
    logProperties['ctxPred'] = ctxPred
    logProperties['evnPred'] = evnPreds

    try:
        mp.track(distinct_id, name, logProperties)
    except Exception, e:
        print 'logContextPrediction failed'
        print e


def logTrainResult(trainStartTime, clfName, paramName, cScore):
    distinct_id = 0
    name = 'train_log'
    logProperties = {}

    logProperties['trainStarted'] = trainStartTime
    logProperties['clfName'] = clfName
    logProperties['paramName'] = paramName
    logProperties['cScore'] = cScore.tolist()

    try:
        mp.track(distinct_id, name, logProperties)
    except Exception, e:
        print 'logTrainResult failed'
        print e

