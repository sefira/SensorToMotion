class classifier:

    # Multinomial Naive Bayes Classifier  
    def naive_bayes_classifier(self,train_x, train_y):  
        from sklearn.naive_bayes import MultinomialNB  
        model = MultinomialNB(alpha=0.01)  
        model.fit(train_x, train_y)  
        return model  
      
      
    # KNN Classifier  
    def knn_classifier(self,train_x, train_y):  
        from sklearn.neighbors import KNeighborsClassifier  
        model = KNeighborsClassifier()  
        model.fit(train_x, train_y)  
        return model  
      
      
    # Logistic Regression Classifier  
    def logistic_regression_classifier(self,train_x, train_y):  
        from sklearn.linear_model import LogisticRegression  
        model = LogisticRegression(penalty='l2')  
        model.fit(train_x, train_y)  
        return model  
      
      
    # Random Forest Classifier  
    def random_forest_classifier(self,train_x, train_y):  
        from sklearn.ensemble import RandomForestClassifier  
        model = RandomForestClassifier(n_estimators=16)  
        model.fit(train_x, train_y)  
        return model  
      
      
    # Decision Tree Classifier  
    def decision_tree_classifier(self,train_x, train_y):  
        from sklearn import tree  
        model = tree.DecisionTreeClassifier()  
        model.fit(train_x, train_y)  
        return model  
      
      
    # GBDT(Gradient Boosting Decision Tree) Classifier  
    def gradient_boosting_classifier(self,train_x, train_y):  
        from sklearn.ensemble import GradientBoostingClassifier  
        model = GradientBoostingClassifier(n_estimators=200)  
        model.fit(train_x, train_y)  
        return model  
      
      
    # SVM Classifier  
    def svm_classifier(self,train_x, train_y):  
        from sklearn.svm import SVC  
        model = SVC(kernel='rbf', probability=True)  
        model.fit(train_x, train_y)  
        return model  
      
    # SVM Classifier using cross validation  
    def svm_cross_validation(self,train_x, train_y):  
        from sklearn.grid_search import GridSearchCV  
        from sklearn.svm import SVC  
        model = SVC(kernel='rbf', probability=True)  
        param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}  
        grid_search = GridSearchCV(model, param_grid, n_jobs = 1, verbose=1)  
        grid_search.fit(train_x, train_y)  
        best_parameters = grid_search.best_estimator_.get_params()  
        for para, val in best_parameters.items():  
            print para, val  
        model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)  
        model.fit(train_x, train_y)  
        return model  

# end of class classifier define 

###########################################
## start to extract featrue and classify ##
###########################################

#m_splitdata = extractFeature.m_splitdata
#m_startPoints = extractFeature.startPoints
#m_name = readData.name
#
#def ExtractFeatureFromTrain():
#    print "extract feature from train data"
#    UnnormalizedData = m_splitdata.GetAllUnnormalizedData()
#    #a = UnnormalizedData.copy()
#    UnnormalizedData[m_name[0]] = UnnormalizedData[m_name[0]] / 2048
#    UnnormalizedData[m_name[1]] = UnnormalizedData[m_name[1]] / 2048
#    UnnormalizedData[m_name[2]] = UnnormalizedData[m_name[2]] / 2048
#    UnnormalizedData[m_name[3]] = UnnormalizedData[m_name[3]] / 1879.44
#    UnnormalizedData[m_name[4]] = UnnormalizedData[m_name[4]] / 1879.44
#    UnnormalizedData[m_name[5]] = UnnormalizedData[m_name[5]] / 1879.44
#    
#    featureOfSensor = []
#    for i in range(len(m_startPoints)-1):
#        featureOfSensor.append([])
#        
#    windowWidth = 100
#    m_featureExtractor = extractFeature.featureExtractor()
#    for classIndex in range(len(m_startPoints)-1):
#        numLimit = 50
#        numCount = 0
#        for startPos in m_startPoints[classIndex]:
#            #if classIndex == 4:
#                #print startPos
#            if numCount < numLimit:
#                numCount = numCount + 1
#                tempFeature = m_featureExtractor.ExtractTradFeature(
#                    UnnormalizedData.loc[startPos-1:startPos+windowWidth-2])
#                featureOfSensor[classIndex].append(tempFeature)
#            else:
#                break
#    return featureOfSensor
#    
#def ExtractFeatureFromTest():
#    print "extract feature from test data"
#    UnnormalizedData = m_splitdata.GetAllUnnormalizedData()
#    #a = UnnormalizedData.copy()
#    UnnormalizedData[m_name[0]] = UnnormalizedData[m_name[0]] / 2048
#    UnnormalizedData[m_name[1]] = UnnormalizedData[m_name[1]] / 2048
#    UnnormalizedData[m_name[2]] = UnnormalizedData[m_name[2]] / 2048
#    UnnormalizedData[m_name[3]] = UnnormalizedData[m_name[3]] / 1879.44
#    UnnormalizedData[m_name[4]] = UnnormalizedData[m_name[4]] / 1879.44
#    UnnormalizedData[m_name[5]] = UnnormalizedData[m_name[5]] / 1879.44
#    
#    featureOfSensor = []        
#    windowWidth = 100
#    m_featureExtractor = extractFeature.featureExtractor()
#    classIndex = len(m_startPoints) - 1
#    numCount = 0
#    for startPos in m_startPoints[classIndex]:
#        numCount = numCount + 1
#        tempFeature = m_featureExtractor.ExtractTradFeature(
#            UnnormalizedData.loc[startPos-1:startPos+windowWidth-2])
#        featureOfSensor.append(tempFeature)
#    return featureOfSensor
#
#m_classifier = classifier()
#m_classifiers_name = ['KNN', 'LR', 'RF', 'DT', 'SVM', 'GBDT']  
#m_classifiers = {'KNN':m_classifier.knn_classifier,  
#               'LR':m_classifier.logistic_regression_classifier,  
#               'RF':m_classifier.random_forest_classifier,  
#               'DT':m_classifier.decision_tree_classifier,  
#              'SVM':m_classifier.svm_classifier,   
#             'GBDT':m_classifier.gradient_boosting_classifier  
#             }  
#
#def TraininAllClassifiers(train_data,train_label,test_data,test_label):
#    num_train = len(train_data)
#    num_feat = len(train_data[0])
#    num_test = len(test_data)
#    num_feat = len(test_data[0])
#    print '******************** Data Info *********************'  
#    print '#training data: %d, #testing_data: %d, dimension: %d' % (num_train, num_test, num_feat)  
#    
#    for classifier_name in m_classifiers_name:  
#        print '******************* %s ********************' % classifier_name  
#        start_time = time.time()  
#        m_classifiers[classifier_name] = m_classifiers[classifier_name](train_data, train_label)  
#        print 'training took %fs!' % (time.time() - start_time)  
#        predict = m_classifiers[classifier_name].predict(test_data)
#        accuracy = metrics.accuracy_score(test_label, predict)  
#        print 'accuracy: %.2f%%' % (100 * accuracy)
#        
#def PrediectinAllClassifiers(test_data):
#    num_test = len(test_data)
#    num_feat = len(test_data[0])
#    print '******************** Data Info *********************'  
#    print '#testing_data: %d, dimension: %d' % (num_test, num_feat)  
#    predictRes = {'KNN':[],  
#               'LR':[],  
#               'RF':[],  
#               'DT':[],  
#              'SVM':[],  
#             'GBDT':[]  
#             }  
#    for classifier_name in m_classifiers_name: 
#        for i in range(len(test_data)):
#            predictRes[classifier_name] = \
#                 m_classifiers[classifier_name].predict(test_data)
#    return predictRes        
#              
## get feature of train and test              
#try:
#    #notexist
#    featureOfTrain
#    featureOfTest
#except NameError:
#    featureOfTrain = ExtractFeatureFromTrain()
#    featureOfTest = ExtractFeatureFromTest()
#else:
#    print "Feature has been extracted!"
#
## reshape train data and train the model
#train_data = []
#train_label = []
#test_data = []
#test_label = []
#for i in range(len(featureOfTrain)):
#    testNum = 5
#    for j in range(len(featureOfTrain[i])-testNum):
#        train_data.append(featureOfTrain[i][j])
#        train_label.append(i+1)
#    for j in range(len(featureOfTrain[i])-testNum,len(featureOfTrain[i])):
#        test_data.append(featureOfTrain[i][j])
#        test_label.append(i+1)
#TraininAllClassifiers(train_data,train_label,test_data,test_label)
#
## no need to reshape test data and predict
#test_data = featureOfTest
#
#try:
#    notexist
#    predictRes
#except NameError:
#    predictRes = PrediectinAllClassifiers(test_data)
#else:
#    print "Predict has been extracted!"
#
## get the mode of different classifiers, present a vote function
#def ModethePredict():
#    from scipy.stats import mode
#    predictMode = []
#    for i in range(len(test_data)):
#        predictMode.append(
#            mode([predictRes['LR'][i],
#                  predictRes['KNN'][i],predictRes['KNN'][i],predictRes['KNN'][i],
#                predictRes['RF'][i],
#                predictRes['GBDT'][i]])[0][0])
#    return predictMode
#
#m_predictMode = ModethePredict()
#from visualizePredictResult import PlotTestSeqandPredictRes
#PlotTestSeqandPredictRes(m_predictMode)
#print "hahaha haizai classificaction"