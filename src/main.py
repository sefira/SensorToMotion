import readData
import splitData
import extractFeature
import classification

from sklearn import metrics
import time

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
## start to extract featrue and classify ##
############################################

m_classifier = classification.classifier()
m_classifiers_name = ['KNN', 'LR', 'RF', 'DT', 'GBDT']  
m_classifiers = {'KNN':m_classifier.knn_classifier,  
               'LR':m_classifier.logistic_regression_classifier,  
               'RF':m_classifier.random_forest_classifier,  
               'DT':m_classifier.decision_tree_classifier,  
              'SVM':m_classifier.svm_classifier,   
             'GBDT':m_classifier.gradient_boosting_classifier  
             }  

def TraininAllClassifiers(train_data,train_label,test_data,test_label):
    num_train = len(train_data)
    num_feat = len(train_data[0])
    num_test = len(test_data)
    num_feat = len(test_data[0])
    print '******************** Data Info *********************'  
    print '#training data: %d, #testing_data: %d, dimension: %d' % (num_train, num_test, num_feat)  
    
    for classifiers_name_it in m_classifiers_name:  
        print '******************* %s ********************' % classifiers_name_it  
        start_time = time.time()  
        m_classifiers[classifiers_name_it] = m_classifiers[classifiers_name_it](train_data, train_label)  
        print 'training took %fs!' % (time.time() - start_time)  
        predict = m_classifiers[classifiers_name_it].predict(test_data)
        accuracy = metrics.accuracy_score(test_label, predict)  
        print 'accuracy: %.2f%%' % (100 * accuracy)
        
def PrediectinAllClassifiers(test_data):
    num_test = len(test_data)
    num_feat = len(test_data[0])
    print '******************** Data Info *********************'  
    print '#testing_data: %d, dimension: %d' % (num_test, num_feat)  
    predictRes = {'KNN':[],  
               'LR':[],  
               'RF':[],  
               'DT':[],  
             'GBDT':[]  
             }  
    for classifier_name in m_classifiers_name: 
        print "%s is predicting" % (classifier_name)
        for i in range(len(test_data)):
            predictRes[classifier_name] = \
                 m_classifiers[classifier_name].predict(test_data)
    return predictRes        
              
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
    testSampleNum = 5
    for j in range(len(featureOfTrain[i])-testSampleNum):
        train_data.append(featureOfTrain[i][j])
        train_label.append(label_numlabel[label_name[i]])
    for j in range(len(featureOfTrain[i])-testSampleNum,len(featureOfTrain[i])):
        test_data.append(featureOfTrain[i][j])
        test_label.append(label_numlabel[label_name[i]])
TraininAllClassifiers(train_data,train_label,test_data,test_label)

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
                  predictRes['KNN'][i]#,predictRes['KNN'][i],predictRes['KNN'][i],
                #predictRes['RF'][i]#,
                #predictRes['GBDT'][i]
                ])[0][0])
    return predictMode

m_predictMode = ModethePredict()
from visualizePredictResult import PlotTestSeqandPredictRes
PlotTestSeqandPredictRes(normalizedSeqs[len(normalizedSeqs)-1]['accelerometerX'],m_predictMode)
