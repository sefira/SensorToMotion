from readData import *

sensorData, normalizedSensorData = ReadData()

motionStartTime = [3650,19700,34000,49240,60800,92500,121200]
motionEndTime = [17650,32000,47100,58000,89200,120400,149000]

stayDribbleSeq = normalizedSensorData[motionStartTime[0]:motionEndTime[0]]
runDribbleSeq = normalizedSensorData[motionStartTime[1]:motionEndTime[1]]
walkSeq = normalizedSensorData[motionStartTime[2]:motionEndTime[2]]
runSeq = normalizedSensorData[motionStartTime[3]:motionEndTime[3]]
shootSeq = normalizedSensorData[motionStartTime[4]:motionEndTime[4]]
jumpSeq = normalizedSensorData[motionStartTime[5]:motionEndTime[5]]
testSeq = normalizedSensorData[motionStartTime[6]:motionEndTime[6]]

# now the most important thing is to split ShootSeq and Jump

def GetSeqStartandEnd(sequence):
    temparr = sequence.index.values
    start = temparr.min()
    end = temparr.max()
    return (start,end)

def GetStartPointsForContinueSeq(sequence):
    startPoints = []
    start,end = GetSeqStartandEnd(sequence)
    if (end - start < 50):
        return startPoints
    step = 50
    for i in range(start,end,step):
        startPoints.append(i)
    return startPoints
    
def GetStartPointsForShootSeq(sequence,thre,dela):
    startPoints = []
    start,end = GetSeqStartandEnd(sequence)
    if(end - start < 50):
        return startPoints
    step = 50
    startPoints.append(start - step*6)
    for i in range(start,end):
        if (sensorData['accelerometerX'].loc[i] > thre) and ((i - startPoints[-1]) > 6*step):
        #if (sequence.loc[i][1] > thre) and ((i - startPoints[-1]) > 6*step):
            startPoints.append(i + dela)
    del startPoints[0]
    return startPoints

def GetStartPointsForJumpSeq(sequence,thre,dela):
    startPoints = []
    start,end = GetSeqStartandEnd(sequence)
    if(end - start < 50):
        return startPoints
    step = 50
    startPoints.append(start - step*6)
    for i in range(start,end):
        if (sensorData['accelerometerX'].loc[i] < thre) and ((i - startPoints[-1]) > 6*step):
        #if (sequence.loc[i][1] > thre) and ((i - startPoints[-1]) > 6*step):
            startPoints.append(i + dela)
    del startPoints[0]
    return startPoints
    
def GetAllSeqStartPoints():
    #threshold = [0,0,-0,-0,(2500-1855.7587801291988)/2254.034829804072,(-1000-1855.7587801291988)/2254.034829804072]
    threshold = [0,0,-0,-0,2500,-1000]
    delay = [0,0,0,0,50,20]
    stayDribbleStartPoints = GetStartPointsForContinueSeq(stayDribbleSeq)
    runDribbleStartPoints = GetStartPointsForContinueSeq(runDribbleSeq)
    walkStartPoints = GetStartPointsForContinueSeq(walkSeq)
    runStartPoints = GetStartPointsForContinueSeq(runSeq)
    
    #for shoot
    shootStartPoints = GetStartPointsForShootSeq(shootSeq,threshold[4],delay[4])
    #for jump
    jumpStartPoints = GetStartPointsForJumpSeq(jumpSeq,threshold[5],delay[5])
    
    testStartPoints = GetStartPointsForContinueSeq(testSeq)    
    return (stayDribbleStartPoints,runDribbleStartPoints,walkStartPoints,
            runStartPoints,shootStartPoints,jumpStartPoints,
            testStartPoints)
            
def GetAllNormalizedSeqs():
    return (stayDribbleSeq,runDribbleSeq,walkSeq,runSeq,
            shootSeq,jumpSeq,testSeq)

def GetAllUnnormalizedSeqs():
    UnnormalizedSeqs = []
    for i in range(len(motionStartTime)):
        UnnormalizedSeqs.append(
            sensorData[motionStartTime[i]:motionEndTime[i]])
    return UnnormalizedSeqs
'''
def GetDiscreteStartPoints(sequence):
    start,end = GetSeqStartandEnd()
    startPoints = []
    window = 100
    thre = 100
    step = 50
    if (end - start < window):
        return startPoints
    #compute the std in step:window
    flagArr = [None] * (end - start)
    flagArr.fi
    i = start
    while  i < end:
        tempSeq = sequence[i:i+window]
        #if(tempSeq.std() < thre):
'''       