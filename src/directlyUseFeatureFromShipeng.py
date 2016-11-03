from os import listdir
from os.path import isfile, join
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
##### read already ectract feature ########
###########################################
print "read feature:"
train_path = '../data/train'
train_files = [f for f in listdir(train_path) if isfile(join(train_path, f))]
test_path = '../data/test'
test_files = [f for f in listdir(test_path) if isfile(join(test_path, f))]

feature_of_train = [0] * len(train_files)
label_of_train = [0] * len(train_files)
for i in range(len(train_files)):
    feature_of_train[i] = pd.read_csv(train_path+"/"+train_files[i],header=None,delim_whitespace=True)
    label_of_train[i] = feature_of_train[i][0]
    feature_of_train[i].drop(0,axis=1, inplace=True)
    
feature_of_test = [0] * len(test_files)
label_of_test = [0] * len(test_files)
for i in range(len(test_files)):
    feature_of_test[i] = pd.read_csv(test_path+"/"+test_files[i],header=None,delim_whitespace=True)
    label_of_test = feature_of_test[i][0]
    feature_of_test[i].drop(0,axis=1, inplace=True)
###########################################
####### start to train and classify #######
###########################################

# reshape train data and train the model
train_data = pd.DataFrame()
train_label = []
test_data = pd.DataFrame()
test_label = []

print "reshape feature:"
for i in range(len(feature_of_train)):
    for j in range(len(feature_of_train[i])):
        train_data = train_data.append(feature_of_train[i].loc[j])
        train_label.append(label_of_train[i].loc[j])
        
for i in range(len(feature_of_test)):
    for j in range(len(feature_of_test[i])):
        test_data = test_data.append(feature_of_test[i].loc[j])
        
###########################################
############# normalize data ##############
###########################################
train_data_bk = train_data
print "normalize feature:"
m_normalizer = processingFeature.Normalizer("robust",train_data)
train_data = m_normalizer.normalizer(train_data)
test_data = m_normalizer.normalizer(test_data)

print "PCA feature:"
m_pcaor = processingFeature.PCAor("normal",train_data,50)
train_data = m_pcaor.pcaor(train_data)
test_data = m_pcaor.pcaor(test_data)

#print "cross validation:"
#m_cross_validation_score = CrossValidateClassifiers(m_classifiers,times=20,num_fold=2,train_data=train_data,train_label=train_label)
#for m_classifiers_name_it in m_classifiers_name:
#    print "%s score : %f" % (m_classifiers_name_it, m_cross_validation_score[m_classifiers_name_it])

print "training classifiers:"
TraininAllClassifiers(m_classifiers,train_data,train_label,train_data,train_label)

save_classifiers(m_classifiers)
###########################################
###### preditct and show the result #######
###########################################  
try:
    notexist
    predict_res
except NameError:
    print "testing in real test data:"
    predict_res = PrediectinAllClassifiers(m_classifiers,test_data)
else:
    print "Predict has been extracted!"
m_predictMode = ModethePredict(test_data,predict_res)
predictSeq = pd.DataFrame(test_data[:,1])
PlotTestSeqandPredictRes(predictSeq,m_predictMode,'MODE')

df = pd.DataFrame(m_predictMode)
df = df.T
df.to_csv("../prefile",sep=' ',index = False,header =False)

# save center and scalar to file 
#m_cent = m_normalizer.robust_scaler.center_
#m_scal = m_normalizer.robust_scaler.scale_
#m_cent = pd.DataFrame(m_cent)
#m_scal = pd.DataFrame(m_scal)
#m_cent.to_csv("../center",sep=' ',index = False,header =False)
#m_scal.to_csv("../scalar",sep=' ',index = False,header =False)

# save pca component to file 
#m_mean = m_pcaor.normal_pca.mean_ 
#m_component = m_pcaor.normal_pca.components_
#m_component = pd.DataFrame(m_component)
#m_mean = pd.DataFrame(m_mean)
#m_component.to_csv("../component",sep=' ',index = False,header =False)
#m_mean.to_csv("../pca_mean",sep=' ',index = False,header =False)

# manuall classifier
m_coef_ = (m_classifiers['LR'].coef_)
m_intercept_ = (m_classifiers['LR'].intercept_)
i = 0
print (train_data[i].dot(m_coef_.T)+m_intercept_.T).argmax(axis=0)
print train_label[i]

# save coeffient and intercept to file 
m_coef_ = pd.DataFrame(m_classifiers['LR'].coef_)
m_intercept_ = pd.DataFrame(m_classifiers['LR'].intercept_)
m_coef_.to_csv("../LR_coef_",sep=' ',index = False,header =False)
m_intercept_.to_csv("../LR_intercept_",sep=' ',index = False,header =False)
