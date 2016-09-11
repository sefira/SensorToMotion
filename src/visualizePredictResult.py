import matplotlib.pyplot as plt
    
def PlotTestSeqandPredictRes(testSeq,predict,title):
    predictSeq = testSeq.copy()
    step = 50
    cursor = predictSeq.index.min()
    for i in range(len(predict)):
        for j in range(step):
            predictSeq[cursor] = predict[i]
            cursor = cursor + 1
    
    plt.figure()
    plt.plot(testSeq,'b-')
    plt.plot(predictSeq,'r^')
    plt.title(title)    