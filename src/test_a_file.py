import readData
import splitData
import extractFeature
import processingFeature
from classification import PrediectinAllClassifiers
from classification import ModethePredict
from classification import load_classifiers
from visualizePredictResult import PlotTestSeqandPredictRes
from sklearn import cross_validation
import pandas as pd

#################################################
######## read a given file data to test #########
#################################################
filename = "216_0805_2.csv"
test_filename = '../data/' + filename
test_sensorData,test_normalizedSensorData = readData.ReadData(test_filename)

m_split_testdata = splitData.splitData(test_sensorData,test_normalizedSensorData)
m_startPoints_testdata = m_split_testdata.GetStartPointsForContinueSeq(test_sensorData)
m_normalized_testdata = m_split_testdata.GetAllNormalizedData()
    
###########################################
######## start to extract featrue  ########
###########################################

# get feature of train and test  import utils
import utils
postfix = 'Datadiv2048_featureUnnor_multiWindow'
featureOf_Train = utils.readListfromCSV(9,'featureOf_Train_' + postfix)
try:
    featureOf_TestinReal = utils.readDataFramefromCSV('featureOf_TestinReal_'+postfix+"_"+filename)
except IOError:    
    m_featureExtractor = extractFeature.MultiWindowDatafeatureExtractor()
    m_testdata = m_normalized_testdata
    print "extract feature from test data in real"
    featureOf_TestinReal = m_featureExtractor.ExtractFeatureinShipengStyle(
                                    m_testdata,
                                    m_startPoints_testdata,False)
    utils.saveDataFrametoCSV(featureOf_TestinReal,'featureOf_TestinReal_'+postfix+"_"+filename)

else:
    print "Feature has been loaded!"
#####################################################
####### load train feature for stdarize & pca #######
#####################################################
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
print "normalize feature:"
m_normalizer = processingFeature.Normalizer("robust",train_data)
train_data = m_normalizer.normalizer(train_data)
featureOf_TestinReal = m_normalizer.normalizer(featureOf_TestinReal)

print "PCA feature:"
m_pcaor = processingFeature.PCAor("normal",train_data,50)
train_data = m_pcaor.pcaor(train_data)
featureOf_TestinReal = m_pcaor.pcaor(featureOf_TestinReal)

train_data,test_data,train_label,test_label = cross_validation.train_test_split(
                            train_data, train_label, test_size=0.1)

m_classifiers = load_classifiers()
###########################################
###### preditct and show the result #######
###########################################
test_realdata = featureOf_TestinReal
predictResinReal = PrediectinAllClassifiers(m_classifiers,test_realdata)
m_predictMode = ModethePredict(test_realdata,predictResinReal)
PlotTestSeqandPredictRes(m_normalized_testdata['accelerometerX'],
                         m_predictMode,'MODE')
df = pd.DataFrame(m_predictMode)
df = df.T
df.to_csv("../prefile",index = False,header =False)