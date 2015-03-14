__author__ = 'jiusi'

projectRoot = '/Users/jiusi/userBehavior/'
dataRoot = projectRoot + 'data/'

motionClfRoot = projectRoot + 'moClf/'
contextClfRoot = projectRoot + 'ctxClf/'
eventClfRoot = projectRoot + 'evnClf/'

motionParamRoot = projectRoot + 'moP/'
contextParamRoot = projectRoot + 'ctxP/'

motionParamPrefix = 'moP'
contextParamPrefix = 'ctxP'

motionClfPrefix = 'moClf'
contextClfPrefix = 'ctxClf'

soundClipPrefix = 'ctxSound'

xmlPath = dataRoot + "dares_g1.1/dares_g1.1_noxmlns.xml"
audioDbJsonPath = dataRoot + "dares_g1.1/audio.json"
audioRoot = dataRoot + "dares_g1.1/dares_g1/"

mp_datetime_format = '%Y-%m-%dT%H:%M:%S'
mp_distinct_id = 'default_distinct_id'

moClf_VH = motionClfRoot + 'moClf_VH/clf.pkl'
moClf_SS_L1 = motionClfRoot + 'moClf_SS_L1/clf.pkl'
moClf_SS_L2A = motionClfRoot + 'moClf_SS_L2A/clf.pkl'
moClf_SS_L2I = motionClfRoot + 'moClf_SS_L2I/clf.pkl'

ctxClf_PROD = contextClfRoot + 'ctxClf_PROD/clf.pkl'
evnClf_PROD = eventClfRoot + 'evnClf_PROD/clf.pkl'

soundClipsRoot = projectRoot + 'requestSoundClips/'

N_MFCC= 13
N_COMPONENTS= 30
N_NEIGHBORS= 3
FREQ_MAX= 10000
K_FOLD= 5
CTX_FRAME_IN_SEC = 5
EVN_FRAME_IN_SEC = 0.2

FEATURES = ['mfcc']

# L1ContextIdNameMap= {
#     "0": "outside",
#     "1": "home",
#     "2": "wild",
#     "3": "reverberant places",
#     "4": "public area",
#     "5": "quite inside"
#   },

L2ContextIdNameMap= {
    "0": "busy street",
    "1": "quite street",
    "2": "bus stop",
    "3": "living room",
    "4": "kitchen",
    "5": "hallway",
    "6": "bedroom",
    "7": "flat",
    "8": "forrest",
    "9": "train station",
    "10": "supermarket",
    "11": "shop",
    "12": "study quite office",
    "13": "subway",
    "14": "walk",
    "15": "in_bus",
    "16": "classroom"
  }

L2L1Map = {
    "0": "3",
    "1": "2",
    "2": "3",
    "3": "0",
    "4": "1",
    "5": "0",
    "6": "0",
    "7": "0",
    "8": "2",
    "9": "3",
    "10": "1",
    "11": "1",
    "12": "0",
    "13": "1",
    "14": "3",
    "15": "3",
    "16": "1"
}

L1ContextIdNameMap = {
    "0": "inside quiet",
    "1": "inside loud",
    "2": "outside quiet",
    "3": "outside loud"
}


L3EventIdNameMap = {
    "0": "unknown",
    "1": "mouse click"
}

# params for motion
GRAN_SAMPLE = 100

STAT_DICT = {'Sitting':0, 'Driving':1, 'Riding':2, 'Walking':3, 'Running': 4}
STAT_NAME = ['Sitting', 'Driving', 'Riding', 'Walking', 'Running']

STAT_CLASS_MAP = {0:0, 1:0, 2:1, 3:1, 4:1}
STAT_CLASS_NAME = {'Inactive':0, 'Active':1}

STAT_CODE = [0, 1, 2, 3, 4]

MIX_PANEL_TOKEN = 'ccd6520fac580540b4a003e6ffa8e2e1'

# feature list for motion train and prediction
FEATURES_SERVICE = range(0,6)


EVN_UNKNOWN = 'unknown'