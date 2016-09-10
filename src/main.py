import readData
import splitData
import extractFeature
from classification import m_classifiers_name
from classification import CrossValidateClassifiers
from classification import TraininAllClassifiers
from classification import PrediectinAllClassifiers

from sklearn import cross_validation

###########################################
########### start to read data ############
###########################################
filename = '../data/216_shipeng_lanqiu2.csv'
sensorData,normalizedSensorData = readData.ReadData(filename)

try:
    m_splitdata
except NameError:
    motionStartTime = [3650,19700,34000,49240,60800,92500,121200]
    motionEndTime = [17650,32000,47100,58000,89200,120400,149000]
    m_splitdata = splitData.splitData(sensorData,normalizedSensorData,motionStartTime,motionEndTime)
    m_startPoints = m_splitdata.GetAllSeqStartPointsForSpecialData()
    normalizedSeqs = m_splitdata.GetAllNormalizedSeqsForSpecialData()
    m_unnormalized_data = m_splitdata.GetAllUnnormalizedData()
else:
    #m_splitdata = splitData()
    print "Data has been split"
    
###########################################
######## start to extract featrue  ########
###########################################
    
# get feature of train and test  
try:
    #notexist
    featureOfTrain
    featureOfTest
except NameError:
    m_featureExtractor = extractFeature.featureExtractor()
    featureOfTrain = m_featureExtractor.ExtractTrainFeatureinShipengStyle(
                                        m_unnormalized_data,m_startPoints,True)
    featureOfTest = m_featureExtractor.ExtractTestFeatureinShipengStyle(
                                        m_unnormalized_data,m_startPoints[len(m_startPoints)-1])
else:
    print "Feature has been extracted!"

###########################################
####### start to train and classify #######
###########################################

# reshape train data and train the model
train_data = []
train_label = []
test_data = []
test_label = []
label_name = ['stayDribble','runDribble','walk','run','shoot','jump']  
label_numlabel = {'stayDribble':1,
                'runDribble':1,
                'walk':4,
                'run':5,
                'shoot':3,
                'jump':6
 }  
for i in range(len(featureOfTrain)):
    for j in range(len(featureOfTrain[i])):
        train_data.append(featureOfTrain[i][j])
        train_label.append(label_numlabel[label_name[i]])
        
m_cross_validation_score = CrossValidateClassifiers(times=20,num_fold=2,train_data=train_data,train_label=train_label)
for m_classifiers_name_it in m_classifiers_name:
    print "%s score : %f" % (m_classifiers_name_it, m_cross_validation_score[m_classifiers_name_it])

train_data,test_data,train_label,test_label = cross_validation.train_test_split(
                            train_data, train_label, test_size=0.5)
TraininAllClassifiers(train_data,train_label,test_data,test_label)

###########################################
###### preditct and show the result #######
###########################################
# no need to reshape test data and predict
test_data = featureOfTest

try:
    #notexist
    predictRes
except NameError:
    predictRes = PrediectinAllClassifiers(test_data)
else:
    print "Predict has been extracted!"

# get the mode of different classifiers, present a vote function
def ModethePredict():
    from scipy.stats import mode
    predictMode = []
    for i in range(len(test_data)):
        predictMode.append(
            mode([#predictRes['LR'][i],
                  predictRes['KNN'][i],#predictRes['KNN'][i],predictRes['KNN'][i],
                predictRes['RF'][i],
                predictRes['GBDT'][i]
                ])[0][0])
    return predictMode

#/m_predictMode = ModethePredict()
from visualizePredictResult import PlotTestSeqandPredictRes
#/PlotTestSeqandPredictRes(normalizedSeqs[len(normalizedSeqs)-1]['accelerometerX'],m_predictMode)
