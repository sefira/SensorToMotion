import splitData
import readData
name = readData.name
originalName = name[:]
name.append('acc')
name.append('gxyz')

import numpy as np
import pandas as pd

try:
    m_splitdata
except NameError:
    m_splitdata = splitData.splitData()
    startPoints = m_splitdata.GetAllSeqStartPoints()
    normalizedSeqs = m_splitdata.GetAllNormalizedSeqs()
    unNormalizedSeqs = m_splitdata.GetAllUnnormalizedSeqs()
else:
    #m_splitdata = splitData()
    print "Data has been split"
    
copydata = 0
flag = 1
class featureExtractor:
    def ExtractFeature(self,data):
        data = pd.concat([data],ignore_index=True)
        m_absData = np.abs(data)
        lengthOfData = len(data)
        step = 50
        windowWidth = 100
        data['acc'] = np.sqrt(np.square(data[name[0]])+
            np.square(data[name[1]])+
            np.square(data[name[2]]))
        data['gxyz'] = (np.abs(data[name[3]])+
            np.abs(data[name[4]])+
            np.abs(data[name[5]]))
        m_featrue = []  
        for partition in range(0,windowWidth,step):
            # avg
            m_mean = [0] * len(name)
            for i in range(len(name)):
                m_mean[i] = np.mean(data[name[i]][partition:partition+step])
            # var
            m_var = [0] * len(name)
            for i in range(len(name)):
                m_var[i] = np.var(data[name[i]][partition:partition+step])
            # std
            m_std = [0] * len(name)
            for i in range(len(name)):
                m_std[i] = np.std(data[name[i]][partition:partition+step])
            # max
            m_max = [0] * len(name)
            for i in range(len(name)):
                m_max[i] = np.max(data[name[i]][partition:partition+step])
            # min
            m_min = [0] * len(name)
            for i in range(len(name)):
                m_min[i] = np.min(data[name[i]][partition:partition+step])
            # sumslp ??? sum of substraction in dislocation
            m_sumslp = [0] * len(name)
            for i in range(len(name)):
                disLocationPre = pd.concat([data[name[i]][partition+1:partition+step-1]],ignore_index=True)
                disLocationPost = pd.concat([data[name[i]][partition:partition+step-2]],ignore_index=True)
                m_sumslp[i] = np.sum(disLocationPre - disLocationPost)/2
            # correlative coefficient
            m_cor = [0] * ((len(originalName) * (len(originalName) - 1))/2)
            #m_fft = [0] * len(originalName)
            #m_energy = [0] * len(originalName)
            corrCount = 0
            for i in range(len(originalName)):
                for j in range(i+1,len(originalName)):
                    m_cor[corrCount] = np.sum(
                    (data[name[i]][partition:partition+step] - m_mean[i]).
                    mul(data[name[j]][partition:partition+step] - 
                    m_mean[j])                            
                        ) / (step - 1)
                    corrCount = corrCount + 1
                #m_fft[i] = np.abs(np.fft.fft(data[name[i]][partition:partition+step]))
                #m_energy[i] = np.sum(np.square(m_fft[i])) / step
            # sum up
            m_up = [0] * len(name)
            m_sumup = [0] * len(originalName)
            for i in range(partition,partition+step-1):
                for j in range(len(name)):
                    if data[name[j]][i+1] > data[name[j]][i]:
                        m_up[j] = m_up[j] + 1
                        if j < len(m_sumup):                        
                            m_sumup[j] = m_sumup[j] + data[name[j]][i+1] - data[name[j]][i]
            # mean abs
            m_meanabs = [0] * len(originalName)
            m_div = [0] * len(originalName)
            for i in range(len(originalName)):
                m_meanabs[i] = np.mean(m_absData[name[i]][partition:partition+step])
                if i < (len(originalName) / 2):                                        
                    m_div[i] = m_meanabs[i] / m_mean[len(originalName)]
                else:
                    m_div[i] = m_meanabs[i] / m_mean[len(originalName) + 1]
                
            # concat feature
            m_featrue = m_featrue+m_mean+m_var+m_std+m_max+m_min+m_sumslp+m_sumup+m_cor+m_up+m_meanabs+m_div
                
            global flag
            if flag == 1:
                global copydata
                copydata = data
                print len(m_mean)
                print len(m_var)
                print len(m_std)
                print len(m_max)
                print len(m_min)
                print len(m_sumslp)
                print len(m_sumup)
                print len(m_cor)
                print len(m_up)
                print len(m_meanabs)
                print len(m_div)
                #print m_featrue
                flag = flag + 1
        
        return m_featrue
        
             
UnnormalizedData = m_splitdata.GetAllUnnormalizedData()
a = UnnormalizedData.copy()
UnnormalizedData[name[0]] = UnnormalizedData[name[0]] / 2048
UnnormalizedData[name[1]] = UnnormalizedData[name[1]] / 2048
UnnormalizedData[name[2]] = UnnormalizedData[name[2]] / 2048
UnnormalizedData[name[3]] = UnnormalizedData[name[3]] / 1879.44
UnnormalizedData[name[4]] = UnnormalizedData[name[4]] / 1879.44
UnnormalizedData[name[5]] = UnnormalizedData[name[5]] / 1879.44

featureOfSensor = []
for i in range(len(startPoints)):
    featureOfSensor.append([])
    
windowWidth = 100
m_featureExtractor = featureExtractor()
for classIndex in range(len(startPoints)):
    numLimit = 50
    numCount = 0
    for startPos in startPoints[classIndex]:
        #if classIndex == 4:        
            #print startPos
        if numCount < numLimit:
            numCount = numCount + 1
            tempFeature = m_featureExtractor.ExtractFeature(
                UnnormalizedData.loc[startPos-1:startPos+windowWidth-2])
            featureOfSensor[classIndex].append(tempFeature)
        else:
            break
        