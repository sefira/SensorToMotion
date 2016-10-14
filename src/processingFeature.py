import numpy as np
import pandas as pd


class Normalizer:
    def __init__(self, normalizer_type,data):
        print "********** init normalizer **********"
        normalizer_map = {
                "zscore1free":self.normalizeDataMeanStd1free,
                "zscore0free":self.normalizeDataMeanStd0free,
                "minmax":self.normalizeDataMinMax,
                "robust":self.normalizeDataRobust
        }
        from sklearn import preprocessing
        self.normalizer = normalizer_map[normalizer_type]
        self.standrad_scaler = preprocessing.StandardScaler().fit(data)
        self.minmax_scaler = preprocessing.MinMaxScaler().fit(data)
        self.robust_scaler = preprocessing.RobustScaler().fit(data)
        
    def normalizeDataMeanStd1free(self,ori_data):
        print "********** MeanStd1free normalize data ***********"
        if type(ori_data) is list:
            data = ori_data[:]
            for i in range(len(ori_data)):
                data[i] = (ori_data[i] - ori_data[i].mean())/ori_data[i].std()
        else:
            data = ori_data.copy()
            data = (ori_data - ori_data.mean()) / ori_data.std()
        return data
        
    def normalizeDataMeanStd0free(self,ori_data):
        print "********** MeanStd0free normalize data ***********"
        if type(ori_data) is list:
            data = ori_data[:]
            for i in range(len(ori_data)):
                data[i] = pd.DataFrame(self.standrad_scaler.transform(data[i]),
                                    index=data[i].index,columns=data[i].columns)
        else:
            data = ori_data.copy()
            data = pd.DataFrame(self.standrad_scaler.transform(data),
                                 index=data.index,columns=data.columns)
        return data
        
    def normalizeDataMinMax(self,ori_data):
        print "********** Minmax normalize data ***********"
        if type(ori_data) is list:
            data = ori_data[:]
            for i in range(len(ori_data)):
                data[i] = pd.DataFrame(self.minmax_scaler.transform(data[i]),
                                index=data[i].index,columns=data[i].columns)
        else:
            data = ori_data.copy()
            data = pd.DataFrame(self.minmax_scaler.transform(data),
                                index=data.index,columns=data.columns)
        return data
    
    def normalizeDataRobust(self,ori_data):
        print "********** Robust normalize data ***********"
        if type(ori_data) is list:
            data = ori_data[:]
            for i in range(len(ori_data)):
                data[i] = pd.DataFrame(self.robust_scaler.transform(data[i]),
                                index=data[i].index,columns=data[i].columns)
        else:
            data = ori_data.copy()
            data = pd.DataFrame(self.robust_scaler.transform(data),
                                index=data.index,columns=data.columns)
        return data
        
# end of class normalizer define
        
class PCAor:
    def __init__(self,pca_type,data,n_components):
        print "******** init PCAer **********"
        pca_map = {
            "already":self.pcawithalreadydata,
            "normal":self.normalPCA,
            "kernal":self.kernalPCA,
        }
        self.components_index = []
        self.eig_vecs = []
        self.pcaor = pca_map[pca_type]
        
        # normal pca init and fit
        from sklearn.decomposition import PCA
        self.normal_pca = PCA(n_components=n_components,whiten=False)
        self.normal_pca.fit(data)
        # already manually standarize data then pca init and fit
        self._pcawithalreadydatatofit(data,n_components)
        # kernal pca init and fit        
        from sklearn.decomposition import KernelPCA
        self.kernal_pca = KernelPCA(kernel="cosine", gamma=10) #cosine for knn
        self.kernal_pca.fit(data)
    
    # to fit the data then get the principle components
    def _pcawithalreadydatatofit(self,ori_data,n_components):
        print "********** Fit Already data ***********"
        cov_mat = ori_data.T.dot(ori_data)/(ori_data.shape[0]-1)
        eig_vals, eig_vecs = np.linalg.eig(cov_mat)
        tot = eig_vals.sum(axis = 0)
        var_exp = pd.DataFrame(eig_vals/tot)
        var_exp = var_exp.sort_values(by=0, ascending=False)
        self.components_index = var_exp.index[0:n_components]
        self.eig_vecs = eig_vecs[self.components_index]
    
    def pcawithalreadydata(self,ori_data):
        print "********** Transform Already data ***********"
        if type(ori_data) is list:
            data = ori_data[:]
            for i in range(len(ori_data)):
                data[i] = ori_data[i].dot(self.eig_vecs.T)
        else:
            data = ori_data.dot(self.eig_vecs.T)
        return data
    
    def normalPCA(self,ori_data):
        print "********** Normal PCA Transform ***********"  
        if type(ori_data) is list:
            data = ori_data[:]
            for i in range(len(ori_data)):
                data[i] = self.normal_pca.transform(ori_data[i])
        else:
            data = self.normal_pca.transform(ori_data)
        return data
    
    def kernalPCA(self,ori_data):
        print "********** Kernal PCA Transform ***********"
        if type(ori_data) is list:
            data = ori_data[:]
            for i in range(len(ori_data)):
                data[i] = self.kernal_pca.transform(ori_data[i])
        else:
            data = self.kernal_pca.transform(ori_data)
        return data
        
# end of class PCAor define
       