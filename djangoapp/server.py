import os
import sys

from algoMotion import main as algoMo

from algoMotion.stepDetector import stepDetect

from algoContext import predict as algoCtx
from algoContext import utilsData as ctxUD

BASE_PATH = os.path.dirname(__file__)

import yaml
import time
import parameters as param

import algoContext.trainInterface as trainInterface

import utils.utils as utils
import utils.logger as logger

from django import forms

from django.conf import settings
from django.conf.urls import patterns, url
from django.core.management import execute_from_command_line
from django.http import JsonResponse



settings.configure(
    DEBUG=True,
    SECRET_KEY='placerandomsecretkeyhere',
    ROOT_URLCONF=sys.modules[__name__],
    TEMPLATE_DIRS=(
        os.path.join(BASE_PATH, 'templates'),
    ),
     WSGI_APPLICATION = 'app.wsgi.application',
)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()



from django.views.decorators.csrf import csrf_exempt


class UploadFileForm(forms.Form):
    file = forms.FileField()


class PredictForm(forms.Form):
    file = forms.FileField()

    # maxFreq = forms['maxFreq']


@csrf_exempt
def motionPredictByRawData(req):
    if req.method != 'POST':
        result = {}
        result['responseOk'] = False
        result['msg'] = 'request method is not post'
        return JsonResponse(result)

    d = yaml.load(req.body)

    result = {}

    if 'req_id' in d:
        result['req_id'] = d['req_id']

    rawData = None
    X = None
    y2 = -1
    if 'rawData' in d and isinstance(d['rawData'], list):
        rawData = d['rawData']
        clfType = ['SS']
        if 'clfType' in d:
            clfType = d['clfType']

        clfDict = {}
        clfDict['VH'] = moClfVH
        clfDict['SSClf1'] = moClfSS_L1
        clfDict['SSClf2Active'] = moClfSS_L2A
        clfDict['SSClf2Inactive'] = moClfSS_L2I

        try:
            X, y2, result = algoMo.predict_raw_service(rawData, clfDict=clfDict, clfType=clfType)
            result['responseOk'] = True
        except Exception, e:
            result['responseOk'] = False
            result['msg'] = e
    else:
        result['responseOk'] = False
        result['msg'] = 'rawData do not exit or not an array'
        return JsonResponse(result)

    result['stepDetected'] = False
    try:
        stepDetected = stepDetect(rawData)
        result['stepDetected'] = stepDetected
    except ValueError, ve:
        result['msg'] = str(ve)

    logger.logMotionPrediction(param.mp_datetime_format,
                               'motionPredictByRawData',
                               rawData,
                               X,
                               result,
                               y2)

    return JsonResponse(result)


@csrf_exempt
def contextPredictByRawData(req):
    result = {}

    if req.method != 'POST':
        result['msg'] = 'only POST allowed here'
        result['responseOk'] = False
        return JsonResponse(result)

    form = PredictForm(req.POST, req.FILES)
    if not form.is_valid():
        result['msg'] = 'Invalid call'
        result['responseOk'] = False
        return JsonResponse(result)

    fileName = utils.genSoundFileName()
    mp3FilePath = param.soundClipsRoot + fileName
    utils.saveUploadedFile(req.FILES['file'], mp3FilePath)

    featureParam = utils.getFeatureParam4Ctx()

    l2code, l3code = algoCtx.predictMp3(mp3FilePath, ctxClfProd, evnClfProd, featureParam)

    logger.logContextPrediction(param.mp_distinct_id,
                                'contextPredictByRawData',
                                mp3FilePath,
                                l2code,
                                l3code)

    result['l2_code'] = l2code
    result['l2_text'] = ctxUD.getL2Text(l2code)

    result['l1_code'] = ctxUD.getL1Code(l2code)
    result['l1_text'] = ctxUD.getL1Text(l2code)

    result['l3_code'] = -1
    result['l3_text'] = 'under construction'

    result['responseOk'] = True

    return JsonResponse(result)


@csrf_exempt
def getContextClf():
    print 'def getContextClf():'


@csrf_exempt
def getMotionClf():
    print 'def getContextClf():'


@csrf_exempt
def trainContextClf(req):
    result = {}

    if req.method != 'POST':
        result['msg'] = 'only POST allowed here'
        result['responseOk'] = False
        return JsonResponse(result)

    form = UploadFileForm(req.POST, req.FILES)
    if not form.is_valid():
        result['msg'] = 'Invalid call'
        result['responseOk'] = False
        return JsonResponse(result)

    fileName = utils.genContextParamFileName()
    paramSavePath = param.contextParamRoot + fileName
    utils.saveUploadedFile(req.FILES['file'], paramSavePath)

    try:
        trainParam = utils.getTrainParam4Ctx(paramSavePath)
    except:
        result['msg'] = 'uploaded json file can not be decoded'
        result['responseOk'] = False
        return JsonResponse(result)

    clfDirName = utils.genContextClfDir(trainParam['CLF'])
    clfSavePath = param.contextClfRoot + clfDirName + 'clf.pkl'

    result = trainClf(trainParam,
                      paramSavePath,
                      clfSavePath,
                      trainInterface.asyncTrainCtx)

    return JsonResponse(result)


@csrf_exempt
def trainEventClf(req):
    result = {}

    if req.method != 'POST':
        result['msg'] = 'only POST allowed here'
        result['responseOk'] = False
        return JsonResponse(result)

    form = UploadFileForm(req.POST, req.FILES)
    if not form.is_valid():
        result['msg'] = 'Invalid call'
        result['responseOk'] = False
        return JsonResponse(result)

    fileName = utils.genContextParamFileName()
    paramSavePath = param.contextParamRoot + fileName
    utils.saveUploadedFile(req.FILES['file'], paramSavePath)

    try:
        trainParam = utils.getTrainParam4Evn(paramSavePath)
    except:
        result['msg'] = 'uploaded json file can not be decoded'
        result['responseOk'] = False
        return JsonResponse(result)

    clfDirName = utils.genContextClfDir(trainParam['CLF'])
    clfSavePath = param.contextClfRoot + clfDirName + 'clf.pkl'

    result = trainClf(trainParam,
                      paramSavePath,
                      clfSavePath,
                      trainInterface.asyncTrainEvn)

    return JsonResponse(result)

def trainClf(trainParam, paramSavePath, clfSavePath, asyncTrainMethod):
    result = {}

    trainStarted = time.strftime(param.mp_datetime_format)
    asyncTrainMethod(trainParam, paramSavePath, clfSavePath, trainStarted)

    result['clfSavePath'] = clfSavePath
    result['paramSavePath'] = paramSavePath
    result['trainStarted'] = trainStarted
    result['msg'] = 'train in progress'
    result['responseOk'] = True

    return result


@csrf_exempt
def trainMotionClf():
    print 'def trainMotionClf():'

@csrf_exempt
def isAlive(*args):
    result = {}
    result['msg'] = 'alive'
    result['responseOk'] = True
    return JsonResponse(result)


urlpatterns = patterns('',
    # url(r'^motionPredictByFeature/$', motionPredictByFeature),
    url(r'^motionPredictByRawData/$', motionPredictByRawData),
    url(r'^contextPredictByRawData/$', contextPredictByRawData),

    # url(r'^getClf/$', getClf),
    url(r'^trainContextClf/$', trainContextClf),
    url(r'^trainEventClf/$', trainEventClf),
    url(r'^trainMotionClf/$', trainMotionClf),
    url(r'^isAlive/$', isAlive)
)

#load trained motion classifiers
moClfVH, moClfSS_L1, moClfSS_L2A, moClfSS_L2I = utils.loadMotionClfs()

#load trained context classifiers
ctxClfProd = utils.loadContextClfs()
evnClfProd = utils.loadEventClfs()

if __name__ == "__main__":
    execute_from_command_line(sys.argv)

