import matplotlib.pyplot as plt
import numpy as np

# Four axes, returned as a 2-d array
f, axarr = plt.subplots(3, 2)

def PlotTestSeqandPredictRes(x,y,title,testSeq,predict):
    predictSeq = testSeq.copy()
    step = 50
    cursor = predictSeq.index.min()
    for i in range(len(predict)):
        for j in range(step):
            predictSeq[cursor] = predict[i]
            cursor = cursor + 1
    testSeq.plot(style='b-',ax = axarr[x,y])
    predictSeq.plot(style='r^',ax = axarr[x,y])
    axarr[x,y].set_title(title)    
    
PlotTestSeqandPredictRes(0,0,'minmax',m_normalized_traindata.loc[121200:149000]['accelerometerX'], a)

PlotTestSeqandPredictRes(0,1,'interquartile',m_normalized_traindata.loc[121200:149000]['accelerometerX'], aa)
PlotTestSeqandPredictRes(1,0,'minmax',m_normalized_testdata['accelerometerX'],b)

PlotTestSeqandPredictRes(1,1,'interquartile',m_normalized_testdata['accelerometerX'],bb)
PlotTestSeqandPredictRes(2,0,'minmax',m_normalized_catchpassdata.loc[45000:94000]['accelerometerX'],c)

PlotTestSeqandPredictRes(2,1,'interquartile',m_normalized_catchpassdata.loc[45000:94000]['accelerometerX'],cc)

plt.show()