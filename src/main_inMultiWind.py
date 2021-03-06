import readData
import splitData
import extractFeature
import processingFeature
from classification import m_classifiers_name
from classification import m_classifiers
from classification import CrossValidateClassifiers
from classification import TraininAllClassifiers
from classification import PrediectinAllClassifiers
from classification import ModethePredict
from classification import save_classifiers
from visualizePredictResult import PlotTestSeqandPredictRes
from sklearn import cross_validation
import pandas as pd

###########################################
########### start to read data ############
###########################################
train_filename = '../data/216_shipeng_lanqiu2.csv'
train_sensorData,train_normalizedSensorData = readData.ReadData(train_filename)

noise_filename = '../data/216_ganrao1.csv'
noise_sensorData,noise_normalizedSensorData = readData.ReadData(noise_filename)

test_filename = '../data/216_shipeng_lanqiu_test2.csv'
test_sensorData,test_normalizedSensorData = readData.ReadData(test_filename)

catchpass_filename = '../data/253_0909_passcatch.csv'
catchpass_sensorData,catchpass_normalizedSensorData = readData.ReadData(catchpass_filename)

try:
    #notexist
    m_split_traindata
    m_split_noisedata
    m_split_testdata
    m_split_catchpassdata
except NameError:
    motionStartTime = [3650,19700,34000,49240,60800,92500,121200]
    motionEndTime = [17650,32000,47100,58000,89200,120400,149000]
    m_split_traindata = splitData.splitSpecialData(train_sensorData,train_normalizedSensorData,
                                                   motionStartTime,motionEndTime)
    m_startPoints_traindata = m_split_traindata.GetAllSeqStartPointsFor_216_shipeng_lanqiu2()
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
    
    motionStartTime = [3000,45000]
    motionEndTime = [43000,94000]
    m_split_catchpassdata = splitData.splitSpecialData(catchpass_sensorData,catchpass_normalizedSensorData,
                                                       motionStartTime,motionEndTime)
    m_startPoints_catchpassdata = m_split_catchpassdata.GetAllSeqStartPointsFor_253_0909_passcatch()
    m_normalized_catchpassdata = m_split_catchpassdata.GetAllNormalizedData()
    m_unnormalized_catchpassdata = m_split_catchpassdata.GetAllUnnormalizedData()
    
else:
    #m_splittraindata = splitData()
    print "Data has been split!"
    
###########################################
######## start to extract featrue  ########
###########################################

# get feature of train and test  
try:
    import utils
    postfix = 'Datadiv2048_featureUnnor_multiWindow'
    featureOf_Train = utils.readListfromCSV(9,'featureOf_Train_' + postfix)
    featureOf_TestinTrain = utils.readDataFramefromCSV('featureOf_TestinTrain_' + postfix)
    featureOf_Noise = utils.readDataFramefromCSV('featureOf_Noise_' + postfix)
    featureOf_TestinReal = utils.readDataFramefromCSV('featureOf_TestinReal_' + postfix)
    featureOf_CatchPass = utils.readListfromCSV(2,'featureOf_CatchPass_' + postfix)
    featureOf_TestinCatchPass = utils.readDataFramefromCSV('featureOf_TestinCatchPass_' + postfix)
except IOError:    
    m_featureExtractor = extractFeature.MultiWindowDatafeatureExtractor()
    m_traindata = m_normalized_traindata
    m_noisedata = m_normalized_noisedata
    m_testdata = m_normalized_testdata
    m_catchpassdata = m_normalized_catchpassdata
    print "extract feature from train data"
    featureOf_Train = m_featureExtractor.ExtractFeatureinShipengStyle(
                                        m_traindata,
                                        m_startPoints_traindata[0:-1],True)
    print "extract feature from test data in train"
    featureOf_TestinTrain = m_featureExtractor.ExtractFeatureinShipengStyle(
                                        m_traindata,
                                        m_startPoints_traindata[-1],False)
    print "extract feature from noise data"
    featureOf_Noise = m_featureExtractor.ExtractFeatureinShipengStyle(
                                        m_noisedata,
                                        m_startPoints_noisedata,True)
    print "extract feature from test data in real"
    featureOf_TestinReal = m_featureExtractor.ExtractFeatureinShipengStyle(
                                        m_testdata,
                                        m_startPoints_testdata,False)
    print "extract feature from catchpass data"
    featureOf_CatchPass = m_featureExtractor.ExtractFeatureinShipengStyle(
                                        m_catchpassdata,
                                        m_startPoints_catchpassdata[0:-1],True)
    print "extract feature from test data in catchpass"
    featureOf_TestinCatchPass = m_featureExtractor.ExtractFeatureinShipengStyle(
                                        m_catchpassdata,
                                        m_startPoints_catchpassdata[-1],False)
    featureOf_Train.append(featureOf_Noise)
    featureOf_Train.append(featureOf_CatchPass[0])
    featureOf_Train.append(featureOf_CatchPass[1])
    print "save feature in intermedia fold!"
    utils.saveListtoCSV(featureOf_Train,'featureOf_Train_' + postfix)
    utils.saveDataFrametoCSV(featureOf_TestinTrain,'featureOf_TestinTrain_' + postfix)
    utils.saveDataFrametoCSV(featureOf_Noise,'featureOf_Noise_' + postfix)
    utils.saveDataFrametoCSV(featureOf_TestinReal,'featureOf_TestinReal_' + postfix)
    utils.saveListtoCSV(featureOf_CatchPass,'featureOf_CatchPass_' + postfix)
    utils.saveDataFrametoCSV(featureOf_TestinCatchPass,'featureOf_TestinCatchPass_' + postfix)

else:
    print "Feature has been loaded!"
    
###########################################
####### start to train and classify #######
###########################################

# reshape train data and train the model
train_data = pd.DataFrame()
train_label = []
test_data = pd.DataFrame()
test_label = []
label_name = ['stayDribble','runDribble','walk','run','shoot','jump',\
                  'noise','catch','pass']  
label_numlabel = {'stayDribble':1,
                'runDribble':1,
                'walk':4,
                'run':5,
                'shoot':3,
                'jump':6,
                'noise':0,
                'catch':7,
                'pass':8
 }  
for i in range(len(featureOf_Train)):
    for j in range(len(featureOf_Train[i])):
        train_data = train_data.append(featureOf_Train[i].loc[j])
        train_label.append(label_numlabel[label_name[i]])
        
###########################################
############# normalize data ##############
###########################################
train_data_bk = train_data
print "normalize feature:"
m_normalizer = processingFeature.Normalizer("robust",train_data)
train_data = m_normalizer.normalizer(train_data)
featureOf_TestinTrain = m_normalizer.normalizer(featureOf_TestinTrain)
featureOf_TestinReal = m_normalizer.normalizer(featureOf_TestinReal)
featureOf_TestinCatchPass = m_normalizer.normalizer(featureOf_TestinCatchPass)

print "PCA feature:"
m_pcaor = processingFeature.PCAor("normal",train_data,50)
train_data = m_pcaor.pcaor(train_data)
featureOf_TestinTrain = m_pcaor.pcaor(featureOf_TestinTrain)
featureOf_TestinReal = m_pcaor.pcaor(featureOf_TestinReal)
featureOf_TestinCatchPass = m_pcaor.pcaor(featureOf_TestinCatchPass)

#print "cross validation:"
#m_cross_validation_score = CrossValidateClassifiers(m_classifiers,times=20,num_fold=2,train_data=train_data,train_label=train_label)
#for m_classifiers_name_it in m_classifiers_name:
#    print "%s score : %f" % (m_classifiers_name_it, m_cross_validation_score[m_classifiers_name_it])

train_data,test_data,train_label,test_label = cross_validation.train_test_split(
                            train_data, train_label, test_size=0.1)
print "training classifiers:"
TraininAllClassifiers(m_classifiers,train_data,train_label,test_data,test_label)

save_classifiers(m_classifiers)
###########################################
###### preditct and show the result #######
###########################################
test_naivedata = featureOf_TestinTrain
try:
    notexist
    predictRes
except NameError:
    print "testing in train data:"
    predictRes = PrediectinAllClassifiers(m_classifiers,test_naivedata)
else:
    print "Predict has been extracted!"
m_predictMode = ModethePredict(test_naivedata,predictRes)
PlotTestSeqandPredictRes(m_normalized_traindata.loc[121200:149000]['accelerometerX'],
                         m_predictMode,'MODE')
                         
test_realdata = featureOf_TestinReal
try:
    notexist
    predictResinReal
except NameError:
    print "testing in real test data:"
    predictResinReal = PrediectinAllClassifiers(m_classifiers,test_realdata)
else:
    print "Predict has been extracted!"
m_predictMode = ModethePredict(test_realdata,predictResinReal)
PlotTestSeqandPredictRes(m_normalized_testdata['accelerometerX'],
                         m_predictMode,'MODE')

test_catchpassdata = featureOf_TestinCatchPass
try:
    notexist
    predictResinCatchPass
except NameError:
    print "testing in catchpass data:"
    predictResinCatchPass = PrediectinAllClassifiers(m_classifiers,test_catchpassdata)
else:
    print "Predict has been extracted!"
m_predictMode = ModethePredict(test_catchpassdata,predictResinCatchPass)
PlotTestSeqandPredictRes(m_normalized_catchpassdata.loc[45000:94000]['accelerometerX'],
                         m_predictMode,'MODE')
                     
                         