class classifier:

    # Multinomial Naive Bayes Classifier  
    def naive_bayes_classifier(self):  
        from sklearn.naive_bayes import MultinomialNB  
        model = MultinomialNB(alpha=0.01) 
        return model  
      
      
    # KNN Classifier  
    def knn_classifier(self):  
        from sklearn.neighbors import KNeighborsClassifier  
        model = KNeighborsClassifier()
        return model  
      
      
    # Logistic Regression Classifier  
    def logistic_regression_classifier(self):  
        from sklearn.linear_model import LogisticRegression  
        model = LogisticRegression(penalty='l2') 
        return model  
      
      
    # Random Forest Classifier  
    def random_forest_classifier(self):  
        from sklearn.ensemble import RandomForestClassifier  
        model = RandomForestClassifier(n_estimators=16) 
        return model  
      
      
    # Decision Tree Classifier  
    def decision_tree_classifier(self):  
        from sklearn import tree  
        model = tree.DecisionTreeClassifier()  
        return model  
      
      
    # GBDT(Gradient Boosting Decision Tree) Classifier  
    def gradient_boosting_classifier(self):  
        from sklearn.ensemble import GradientBoostingClassifier  
        model = GradientBoostingClassifier(n_estimators=200)  
        return model  
      
      
    # SVM Classifier  
    def svm_classifier(self):  
        from sklearn.svm import SVC  
        model = SVC(kernel='rbf', probability=True)  
        return model  
      
    # SVM Classifier using cross validation  
    def svm_cross_validation(self):  
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
        return model  

# end of class classifier define 

