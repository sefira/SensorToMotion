from readData import *

class splitData:        
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
    def GetSeqStartandEnd(self,sequence):
        temparr = sequence.index.values
        start = temparr.min()
        end = temparr.max()
        return (start,end)
    
    def GetStartPointsForContinueSeq(self,sequence):
        startPoints = []
        start,end = self.GetSeqStartandEnd(sequence)
        if (end - start < 50):
            return startPoints
        step = 50
        for i in range(start,end,step):
            startPoints.append(i)
        return startPoints
        
    def GetStartPointsForShootSeq(self,sequence,thre,dela):
        startPoints = []
        start,end = self.GetSeqStartandEnd(sequence)
        if(end - start < 50):
            return startPoints
        step = 50
        startPoints.append(start - step*6)
        for i in range(start,end):
            if (self.sensorData['accelerometerX'].loc[i] > thre) and ((i - startPoints[-1]) > 6*step):
            #if (sequence.loc[i][1] > thre) and ((i - startPoints[-1]) > 6*step):
                startPoints.append(i + dela)
        del startPoints[0]
        return startPoints
    
    def GetStartPointsForJumpSeq(self,sequence,thre,dela):
        startPoints = []
        start,end = self.GetSeqStartandEnd(sequence)
        if(end - start < 50):
            return startPoints
        step = 50
        startPoints.append(start - step*6)
        for i in range(start,end):
            if (self.sensorData['accelerometerX'].loc[i] < thre) and ((i - startPoints[-1]) > 6*step):
            #if (sequence.loc[i][1] > thre) and ((i - startPoints[-1]) > 6*step):
                startPoints.append(i + dela)
        del startPoints[0]
        return startPoints
        
    def GetAllSeqStartPoints(self):
        #threshold = [0,0,-0,-0,(2500-1855.7587801291988)/2254.034829804072,(-1000-1855.7587801291988)/2254.034829804072]
        threshold = [0,0,-0,-0,2500,-1000]
        delay = [0,0,0,0,50,20]
        stayDribbleStartPoints = self.GetStartPointsForContinueSeq(self.stayDribbleSeq)
        runDribbleStartPoints = self.GetStartPointsForContinueSeq(self.runDribbleSeq)
        walkStartPoints = self.GetStartPointsForContinueSeq(self.walkSeq)
        runStartPoints = self.GetStartPointsForContinueSeq(self.runSeq)
        
        #for shoot
        shootStartPoints = self.GetStartPointsForShootSeq(self.shootSeq,threshold[4],delay[4])
        #for jump
        jumpStartPoints = self.GetStartPointsForJumpSeq(self.jumpSeq,threshold[5],delay[5])
        
        testStartPoints = self.GetStartPointsForContinueSeq(self.testSeq)    
        return (stayDribbleStartPoints,runDribbleStartPoints,walkStartPoints,
                runStartPoints,shootStartPoints,jumpStartPoints,
                testStartPoints)
                
    def GetAllNormalizedSeqs(self):
        return (self.stayDribbleSeq,self.runDribbleSeq,self.walkSeq,
                self.runSeq,self.shootSeq,self.jumpSeq,self.testSeq)
    
    def GetAllUnnormalizedSeqs(self):
        UnnormalizedSeqs = []
        for i in range(len(self.motionStartTime)):
            UnnormalizedSeqs.append(
                self.sensorData[self.motionStartTime[i]:self.motionEndTime[i]])
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