from splitData import *
import matplotlib.pyplot as plt

def GetTestSeq():
    m_splitData = splitData()
    tempSeqs = m_splitData.GetAllNormalizedSeqs()
    testSeqs = tempSeqs[len(tempSeqs)-1]
    return testSeqs['accelerometerX']
    
def PlotTestSeqandPredictRes(predict):
    testSeq = GetTestSeq()
    predictSeq = testSeq.copy()
    step = 50
    cursor = predictSeq.index.min()
    for i in range(len(predict)):
        for j in range(step):
            predictSeq[cursor] = predict[i]
            cursor = cursor + 1
    
    plt.plot(testSeq,'b-')
    plt.plot(predictSeq,'r^')