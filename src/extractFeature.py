import readData

import numpy as np
import pandas as pd

augmentationName = readData.sensor_name[:]
originalName = readData.sensor_name[:]
augmentationName.append('acc')
augmentationName.append('gxyz')

copydata = 0
flag = 1
class FeatureExtractor:
    def __init__(self):
        print "******** FeatureExtractor init **********"
        self.sensor_name = readData.sensor_name
        
    def _ExtractTraditonFeature(self,data):
        data = pd.concat([data],ignore_index=True)
        m_absData = np.abs(data)
        step = 50
        windowWidth = 100
        data['acc'] = np.sqrt(np.square(data[augmentationName[0]])+
            np.square(data[augmentationName[1]])+
            np.square(data[augmentationName[2]]))
        data['gxyz'] = (np.abs(data[augmentationName[3]])+
            np.abs(data[augmentationName[4]])+
            np.abs(data[augmentationName[5]]))
        m_featrue = pd.DataFrame()
        for partition in range(0,windowWidth,step):
            # avg
            m_mean = [0] * len(augmentationName)
            for i in range(len(augmentationName)):
                m_mean[i] = np.mean(data[augmentationName[i]][partition:partition+step])
            # var
            m_var = [0] * len(augmentationName)
            for i in range(len(augmentationName)):
                m_var[i] = np.var(data[augmentationName[i]][partition:partition+step])
            # std
            m_std = [0] * len(augmentationName)
            for i in range(len(augmentationName)):
                m_std[i] = np.std(data[augmentationName[i]][partition:partition+step])
            # max
            m_max = [0] * len(augmentationName)
            for i in range(len(augmentationName)):
                m_max[i] = np.max(data[augmentationName[i]][partition:partition+step])
            # min
            m_min = [0] * len(augmentationName)
            for i in range(len(augmentationName)):
                m_min[i] = np.min(data[augmentationName[i]][partition:partition+step])
            # sumslp ??? sum of substraction in dislocation
            m_sumslp = [0] * len(augmentationName)
            for i in range(len(augmentationName)):
                disLocationPre = pd.concat([data[augmentationName[i]][partition+1:partition+step-1]],ignore_index=True)
                disLocationPost = pd.concat([data[augmentationName[i]][partition:partition+step-2]],ignore_index=True)
                m_sumslp[i] = np.sum(disLocationPre - disLocationPost)/2
            # correlative coefficient
            m_cor = [0] * ((len(originalName) * (len(originalName) - 1))/2)
            #m_fft = [0] * len(originalName)
            #m_energy = [0] * len(originalName)
            corrCount = 0
            for i in range(len(originalName)):
                for j in range(i+1,len(originalName)):
                    m_cor[corrCount] = np.sum(
                    (data[augmentationName[i]][partition:partition+step] - m_mean[i]).
                    mul(data[augmentationName[j]][partition:partition+step] - 
                    m_mean[j])                            
                        ) / (step - 1)
                    corrCount = corrCount + 1
                #m_fft[i] = np.abs(np.fft.fft(data[name[i]][partition:partition+step]))
                #m_energy[i] = np.sum(np.square(m_fft[i])) / step
            # sum up
            m_up = [0] * len(augmentationName)
            m_sumup = [0] * len(originalName)
            for i in range(partition,partition+step-1):
                for j in range(len(augmentationName)):
                    if data[augmentationName[j]][i+1] > data[augmentationName[j]][i]:
                        m_up[j] = m_up[j] + 1
                        if j < len(m_sumup):                        
                            m_sumup[j] = m_sumup[j] + data[augmentationName[j]][i+1] - data[augmentationName[j]][i]
            # mean abs
            m_meanabs = [0] * len(originalName)
            m_div = [0] * len(originalName)
            for i in range(len(originalName)):
                m_meanabs[i] = np.mean(m_absData[augmentationName[i]][partition:partition+step])
                if i < (len(originalName) / 2):                                        
                    m_div[i] = m_meanabs[i] / m_mean[len(originalName)]
                else:
                    m_div[i] = m_meanabs[i] / m_mean[len(originalName) + 1]
                
            # concat feature
            #m_featrue = m_featrue+m_mean+m_var+m_std+m_max+m_min+m_sumslp+m_sumup+m_cor+m_up+m_meanabs+m_div
            m_featrue = m_featrue.append(
                    m_mean+m_var+m_std+m_max+m_min+m_sumslp+m_sumup+m_cor+m_meanabs+m_div)
            
#            global flag
#            if flag == 1:
#                global copydata
#                copydata = data
#                print len(m_mean)
#                print len(m_var)
#                print len(m_std)
#                print len(m_max)
#                print len(m_min)
#                print len(m_sumslp)
#                print len(m_sumup)
#                print len(m_cor)
#                print len(m_up)
#                print m_up
#                print len(m_meanabs)
#                print len(m_div)
#                #print m_featrue
#                flag = flag + 1
        m_featrue.reset_index(drop=True,inplace=True)
        m_featrue = m_featrue.T
        return m_featrue
    
    def _DealListData(self,m_data,m_startPoints,needBanlance): 
        windowWidth = 100
        if needBanlance:
            # if need banlance the data, num limitation set to 50,
            # so that (number of shoot samples etc.) = (number of run samples etc.) 
            numLimit = 50
        else:
            numLimit = 999999
        if type(m_startPoints[0]) is list:
            featureOfSensor = []
            for i in range(len(m_startPoints)):
                featureOfSensor.append(pd.DataFrame())
            for classIndex in range(len(m_startPoints)):
                numCount = 0
                for startPos in m_startPoints[classIndex]:
                    if numCount < numLimit:
                        numCount = numCount + 1
                        tempFeature = self._ExtractTraditonFeature(
                            m_data.loc[startPos:startPos+windowWidth-1])
                        featureOfSensor[classIndex] = featureOfSensor[classIndex].append(tempFeature)
                    else:
                        break
                featureOfSensor[classIndex].reset_index(drop=True,inplace=True)
        return featureOfSensor

# end of class FeatureExtractor define

class UnnormaDatafeatureExtractor(FeatureExtractor):
    def __init__(self):
        print "******** UnnormaDatafeatureExtractor init **********"
        self.sensor_name = readData.sensor_name
    def ExtractFeatureinShipengStyle(self,m_unnormalizedData,m_startPoints,needBanlance = True):
        print "********** extract feature from unpreNorma data **********"        
        UnnormalizedData = m_unnormalizedData.copy()
        UnnormalizedData[self.sensor_name[0]] = UnnormalizedData[self.sensor_name[0]] / 2048
        UnnormalizedData[self.sensor_name[1]] = UnnormalizedData[self.sensor_name[1]] / 2048
        UnnormalizedData[self.sensor_name[2]] = UnnormalizedData[self.sensor_name[2]] / 2048
        UnnormalizedData[self.sensor_name[3]] = UnnormalizedData[self.sensor_name[3]] / 1879.44
        UnnormalizedData[self.sensor_name[4]] = UnnormalizedData[self.sensor_name[4]] / 1879.44
        UnnormalizedData[self.sensor_name[5]] = UnnormalizedData[self.sensor_name[5]] / 1879.44
        m_data = UnnormalizedData.copy()
        
        if type(m_startPoints[0]) is list:
            featureOfSensor = self._DealListData(m_data,m_startPoints,needBanlance)
        else:
            featureOfSensor = self._DealListData(m_data,[m_startPoints],needBanlance)
            featureOfSensor = featureOfSensor[0]
        return featureOfSensor

# end of class UnnormaDatafeatureExtractor define

class NormaDatafeatureExtractor(FeatureExtractor):
    def __init__(self):
        self.sensor_name = readData.sensor_name
        print "****** NormaDatafeatureExtractor init ********"

# ExtractFeatureinShipengStyle in NormaDatafeatureExtractor
# use normalizeData from readData()
# instead use unnormalizeData then div 2048 & 1879
    def ExtractFeatureinShipengStyle(self,m_normalizedData,m_startPoints,needBanlance = True):
        print "********** extract feature from preNorma data **********"
        m_data = m_normalizedData.copy()  
        
        if type(m_startPoints[0]) is list:
            featureOfSensor = self._DealListData(m_data,m_startPoints,needBanlance)
        else:
            featureOfSensor = self._DealListData(m_data,[m_startPoints],needBanlance)
            featureOfSensor = featureOfSensor[0]
        return featureOfSensor
        
# end of class NormaDatafeatureExtractor define

# inherit from NormaDatafeatureExtractor
class MultiWindowDatafeatureExtractor(NormaDatafeatureExtractor):
    def __init__(self):
        self.sensor_name = readData.sensor_name
        print "***** MultiWindowDatafeatureExtract init ******"
        
# Extract feature from multi window. There is a window with step 2
# and the same length and center as a normal window
    def move_startpoints_to_mid(self,start_points,windowWidth):
        offset = (windowWidth - 1) / 2
        start_points = [x + offset for x in start_points]
        return start_points
        
    def _DealListData(self,m_data,m_startPoints,needBanlance):
        print "********** multi-windows extract **********"
        windowWidth = 100
        offset = (windowWidth - 1) / 2
        if needBanlance:
            # if need banlance the data, num limitation set to 50,
            # so that (number of shoot samples etc.) = (number of run samples etc.) 
            numLimit = 50
        else:
            numLimit = 999999
        if type(m_startPoints[0]) is list:
            featureOfSensor = []
            for i in range(len(m_startPoints)):
                featureOfSensor.append(pd.DataFrame())
            for classIndex in range(len(m_startPoints)):
                mid_points = self.move_startpoints_to_mid(m_startPoints[classIndex],
                                                         windowWidth)
                numCount = 0
                for mid_point in mid_points:
                    if numCount < numLimit:
                        numCount = numCount + 1
                        normal_range = range(mid_point-offset,mid_point+(offset+1)+1)
                        tempFeature_normal = self._ExtractTraditonFeature(
                            m_data.loc[normal_range])
                        step2_range = [(x - normal_range[len(normal_range)/2])  for x in normal_range]
                        step2_range = [x*2 for x in step2_range]
                        step2_range = [(x + normal_range[len(normal_range)/2])  for x in step2_range]
                        tempFeature_mulit = self._ExtractTraditonFeature(
                            m_data.loc[step2_range])
                        tempFeature = pd.DataFrame()
                        tempFeature = tempFeature.append(tempFeature_normal.T)
                        tempFeature = tempFeature.append(tempFeature_mulit.T)
                        tempFeature = tempFeature.T
                        #print(tempFeature.shape)
                        featureOfSensor[classIndex] = featureOfSensor[classIndex].append(tempFeature)
                    else:
                        break
                featureOfSensor[classIndex].reset_index(drop=True,inplace=True)
        return featureOfSensor
        
# end of class MultiWindowDatafeatureExtractor define
        
        
        