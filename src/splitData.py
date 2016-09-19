class splitData:
    def __init__(self,sensorData, normalizedSensorData):
        self.sensorData = sensorData
        self.normalizedSensorData = normalizedSensorData

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
        for i in range(start,end-100,step):
            startPoints.append(i)
        return startPoints
        
    def GetAllNormalizedData(self):
        return self.normalizedSensorData.copy()
        
    def GetAllUnnormalizedData(self):
        return self.sensorData.copy()
        

class splitSpecialData(splitData):
    def __init__(self,sensorData, normalizedSensorData,motionStartTime,motionEndTime):
        self.sensorData = sensorData
        self.normalizedSensorData = normalizedSensorData
        self.motionStartTime = motionStartTime
        self.motionEndTime = motionEndTime

    # now the most important thing is to split ShootSeq and Jump        
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
        
    def GetAllSeqStartPointsFor_216_shipeng_lanqiu2(self):        
        stayDribbleSeq = self.normalizedSensorData[self.motionStartTime[0]:self.motionEndTime[0]].copy()
        runDribbleSeq = self.normalizedSensorData[self.motionStartTime[1]:self.motionEndTime[1]].copy()
        walkSeq = self.normalizedSensorData[self.motionStartTime[2]:self.motionEndTime[2]].copy()
        runSeq = self.normalizedSensorData[self.motionStartTime[3]:self.motionEndTime[3]].copy()
        shootSeq = self.normalizedSensorData[self.motionStartTime[4]:self.motionEndTime[4]].copy()
        jumpSeq = self.normalizedSensorData[self.motionStartTime[5]:self.motionEndTime[5]].copy()
        testSeq = self.normalizedSensorData[self.motionStartTime[6]:self.motionEndTime[6]].copy()
        
        #threshold = [0,0,-0,-0,(2500-1855.7587801291988)/2254.034829804072,(-1000-1855.7587801291988)/2254.034829804072]
        threshold = [0,0,-0,-0,2500,-1000]
        delay = [0,0,0,0,50,20]
        stayDribbleStartPoints = self.GetStartPointsForContinueSeq(stayDribbleSeq)
        runDribbleStartPoints = self.GetStartPointsForContinueSeq(runDribbleSeq)
        walkStartPoints = self.GetStartPointsForContinueSeq(walkSeq)
        runStartPoints = self.GetStartPointsForContinueSeq(runSeq)
        
        #for shoot
        shootStartPoints = self.GetStartPointsForShootSeq(shootSeq,threshold[4],delay[4])
        #for jump
        jumpStartPoints = self.GetStartPointsForJumpSeq(jumpSeq,threshold[5],delay[5])
        
        testStartPoints = self.GetStartPointsForContinueSeq(testSeq)    
        
        result = []
        result.append(stayDribbleStartPoints)
        result.append(runDribbleStartPoints)
        result.append(walkStartPoints)
        result.append(runStartPoints)
        result.append(shootStartPoints)
        result.append(jumpStartPoints)
        result.append(testStartPoints)
        return result[:]
        
    def GetStartPointsForCatchPassSeq(self,sequence):
        catchStartPoints = []
        passStartPoints = []
        start,end = self.GetSeqStartandEnd(sequence)
        if(end - start < 50):
            return (passStartPoints,catchStartPoints)
        threshold = [1000,4000]
        delay = [30,30]
        step = [50,100]
        catchStartPoints.append(start - step[1]*5)
        passStartPoints.append(start - step[1]*5)
        for i in range(start,end):
            if (self.sensorData['accelerometerX'].loc[i] < threshold[0]) and ((i - catchStartPoints[-1]) > 5*step[1]):
                catchStartPoints.append(i - delay[0] + 1)
                for j in range(i+step[1],i+5*step[1]):
                    if j > 41600:
                        j = j
                    if (self.sensorData['accelerometerX'].loc[j] > threshold[1]):
                        passStartPoints.append(j - delay[1] + 1)
                        break
        del catchStartPoints[0]
        del passStartPoints[0]
        return (catchStartPoints,passStartPoints)
        
    def GetAllSeqStartPointsFor_253_0909_passcatch(self):
        catchpassSeq = self.normalizedSensorData[self.motionStartTime[0]:self.motionEndTime[0]].copy()
        testSeq = self.normalizedSensorData[self.motionStartTime[-1]:self.motionEndTime[-1]].copy()
        
        # for pass and catch
        catchStartPoints,passStartPoints = self.GetStartPointsForCatchPassSeq(catchpassSeq)       
        testStartPoints = self.GetStartPointsForContinueSeq(testSeq)    
        
        result = []
        result.append(catchStartPoints)
        result.append(passStartPoints)
        result.append(testStartPoints)
        return result[:]
                
    def GetAllNormalizedSeqsForSpecialData(self):
        NormalizedSeqs = []
        for i in range(len(self.motionStartTime)):
            NormalizedSeqs.append(
                self.normalizedSensorData[self.motionStartTime[i]:self.motionEndTime[i]])
        return NormalizedSeqs[:]
    
    def GetAllUnnormalizedSeqsForSpecialData(self):
        UnnormalizedSeqs = []
        for i in range(len(self.motionStartTime)):
            UnnormalizedSeqs.append(
                self.sensorData[self.motionStartTime[i]:self.motionEndTime[i]])
        return UnnormalizedSeqs[:]
        
        
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