import readData
import splitData
import extractFeature
from classification import m_classifiers_name
from classification import CrossValidateClassifiers
from classification import TraininAllClassifiers
from classification import PrediectinAllClassifiers
from visualizePredictResult import PlotTestSeqandPredictRes

from sklearn import cross_validation
import pandas as pd
import matplotlib.pyplot as plt

###########################################
########### start to read data ############
###########################################
train_filename = '../data/216_shipeng_lanqiu2.csv'
train_sensorData,train_normalizedSensorData = readData.ReadData(train_filename)

noise_filename = '../data/216_ganrao1.csv'
noise_sensorData,noise_normalizedSensorData = readData.ReadData(noise_filename)

test_filename = '../data/216_shipeng_lanqiu_test2.csv'
test_sensorData,test_normalizedSensorData = readData.ReadData(test_filename)

try:
    m_split_traindata
    m_split_noisedata
    m_split_testdata
except NameError:
    motionStartTime = [3650,19700,34000,49240,60800,92500,121200]
    motionEndTime = [17650,32000,47100,58000,89200,120400,149000]
    m_split_traindata = splitData.splitSpecialData(train_sensorData,train_normalizedSensorData,motionStartTime,motionEndTime)
    m_startPoints_traindata = m_split_traindata.GetAllSeqStartPointsForSpecialData()
    m_normalized_traindata = m_split_traindata.GetAllNormalizedData()
    m_unnormalized_traindata = m_split_traindata.GetAllUnnormalizedData()
    
    m_split_noisedata = splitData.splitData(noise_sensorData,noise_normalizedSensorData)
    m_startPoints_noisedata = m_split_noisedata.GetStartPointsForContinueSeq(noise_sensorData)
    m_normalized_noisedata = m_split_noisedata.GetAllNormalizedData()
    m_unnormalized_noisedata = m_split_noisedata.GetAllUnnormalizedData()
    
    m_split_testdata = splitData.splitData(test_sensorData,test_normalizedSensorData)
    m_startPoints_testdata = m_split_testdata.GetStartPointsForContinueSeq(test_sensorData)
    m_normalized_testdata = m_split_testdata.GetAllNormalizedData()
    m_unnormalized_testdata = m_split_testdata.GetAllUnnormalizedData()
else:
    #m_splittraindata = splitData()
    print "Data has been split!"
    
###########################################
######## start to extract featrue  ########
###########################################

# get feature of train and test  
try:
    import utils
    featureOf_Train = utils.readListfromCSV(7,'featureOf_Train_Datadiv2048_featureUnnor')
    featureOf_TestinTrain = utils.readDataFramefromCSV('featureOf_TestinTrain_Datadiv2048_featureUnnor')
    featureOf_Noise = utils.readDataFramefromCSV('featureOf_Noise_Datadiv2048_featureUnnor')
    featureOf_TestinReal= utils.readDataFramefromCSV('featureOf_TestinReal_Datadiv2048_featureUnnor')
except IOError:
#    m_featureExtractor = extractFeature.featureExtractor()
#    m_traindata = m_unnormalized_traindata
#    m_noisedata = m_unnormalized_noisedata
#    m_testdata = m_unnormalized_testdata
    
    m_featureExtractor = extractFeature.AdvancedFeatureExtractor()
    m_traindata = m_normalized_traindata
    m_noisedata = m_normalized_noisedata
    m_testdata = m_normalized_testdata
    print "extract feature from train data"
    featureOf_Train = m_featureExtractor.ExtractFeatureForSpecialDatainShipengStyle(
                                        m_traindata,
                                        m_startPoints_traindata,True)
    print "extract feature from test data in train"
    featureOf_TestinTrain = m_featureExtractor.ExtractFeatureinShipengStyle(
                                        m_traindata,
                                        m_startPoints_traindata[
                                        len(m_startPoints_traindata)-1],False)
    print "extract feature from noise data"
    featureOf_Noise = m_featureExtractor.ExtractFeatureinShipengStyle(
                                        m_noisedata,
                                        m_startPoints_noisedata,True)
    print "extract feature from test data in real"
    featureOf_TestinReal = m_featureExtractor.ExtractFeatureinShipengStyle(
                                        m_testdata,
                                        m_startPoints_testdata,False)
    featureOf_Train.append(featureOf_Noise)
    print "save feature in intermedia fold!"
    utils.saveListtoCSV(featureOf_Train,'featureOf_Train_Datadiv2048_featureUnnor')
    utils.saveDataFrametoCSV(featureOf_TestinTrain,'featureOf_TestinTrain_Datadiv2048_featureUnnor')
    utils.saveDataFrametoCSV(featureOf_Noise,'featureOf_Noise_Datadiv2048_featureUnnor')
    utils.saveDataFrametoCSV(featureOf_TestinReal,'featureOf_TestinReal_Datadiv2048_featureUnnor')
    
else:
    print "Feature has been loaded!"


###########################################
############# normalize data ##############
###########################################
for i in range(len(featureOf_Train)):
    plt.figure()
    plt.plot(featureOf_Train[i][0])
m_featureExtractor = extractFeature.AdvancedFeatureExtractor()
featureOf_Train = m_featureExtractor.normalizeData(featureOf_Train)
featureOf_TestinTrain = m_featureExtractor.normalizeData(featureOf_TestinTrain)
featureOf_Noise = m_featureExtractor.normalizeData(featureOf_Noise)
featureOf_TestinReal = m_featureExtractor.normalizeData(featureOf_TestinReal)
for i in range(len(featureOf_Train)):
    plt.figure()
    plt.plot(featureOf_Train[i][0])

###########################################
####### start to train and classify #######
###########################################

# reshape train data and train the model
train_data = pd.DataFrame()
train_label = []
test_data = pd.DataFrame()
test_label = []
label_name = ['stayDribble','runDribble','walk','run','shoot','jump','noise']  
label_numlabel = {'stayDribble':1,
                'runDribble':1,
                'walk':4,
                'run':5,
                'shoot':3,
                'jump':6,
                'noise':0
 }  
for i in range(len(featureOf_Train)):
    for j in range(len(featureOf_Train[i])):
        train_data = train_data.append(featureOf_Train[i].loc[j])
        train_label.append(label_numlabel[label_name[i]])

print "cross validation:"
m_cross_validation_score = CrossValidateClassifiers(times=20,num_fold=2,train_data=train_data,train_label=train_label)
for m_classifiers_name_it in m_classifiers_name:
    print "%s score : %f" % (m_classifiers_name_it, m_cross_validation_score[m_classifiers_name_it])

train_data,test_data,train_label,test_label = cross_validation.train_test_split(
                            train_data, train_label, test_size=0.1)
print "training classifiers:"
TraininAllClassifiers(train_data,train_label,test_data,test_label)

###########################################
###### preditct and show the result #######
###########################################
# no need to reshape test data and predict
test_naivedata = featureOf_TestinTrain
test_realdata = featureOf_TestinReal

# get the mode of different classifiers, present a vote function
def ModethePredict(test_data,predictRes):
    from scipy.stats import mode
    predictMode = []
    for i in range(len(test_data)):
        predictMode.append(
            mode([#predictRes['LR'][i],
                  predictRes['KNN'][i],#predictRes['KNN'][i],predictRes['KNN'][i],
                predictRes['RF'][i],
                predictRes['GBDT'][i]#,predictRes['GBDT'][i]
                ])[0][0])
    return predictMode
try:
    notexist
    predictRes
except NameError:
    predictRes = PrediectinAllClassifiers(test_naivedata)
else:
    print "Predict has been extracted!"
m_predictMode = ModethePredict(test_naivedata,predictRes)
PlotTestSeqandPredictRes(m_normalized_traindata.loc[121200:149000]['accelerometerX'],m_predictMode,'MODE')
    
try:
    notexist
    predictResinReal
except NameError:
    print "testing in real test data:"
    predictResinReal = PrediectinAllClassifiers(test_realdata)
else:
    print "Predict has been extracted!"
m_predictMode = ModethePredict(test_realdata,predictResinReal)
PlotTestSeqandPredictRes(m_normalized_testdata['accelerometerX'],m_predictMode,'MODE')
#/PlotTestSeqandPredictRes(m_normalized_testdata['accelerometerX'],predictResinReal['KNN'],'KNN')
#/PlotTestSeqandPredictRes(m_normalized_testdata['accelerometerX'],predictResinReal['LR'],'LR')
#/PlotTestSeqandPredictRes(m_normalized_testdata['accelerometerX'],predictResinReal['RF'],'RF')
#/PlotTestSeqandPredictRes(m_normalized_testdata['accelerometerX'],predictResinReal['GBDT'],'GBDT')
