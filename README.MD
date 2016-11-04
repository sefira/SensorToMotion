# SensorToMotion
Hi! This is a page of a project which takes Sensor signal(3D accelerometer & 3D gyroscope) as trainning data to train some models then prediect what is a basketball athlete doing(e.g. runing, walking, dribbling, shooting, jumpping, catching and passing a ball).

At a word, This is a mechina learning project for [Human Activity Recognition](https://en.wikipedia.org/wiki/Activity_recognition#Sensor-basedn) beased on Sensor data. And a lot of [methods](http://ieeexplore.ieee.org/document/6365160/) have been explored in this domain.

I have did a little bit of try in this domain, too. I will explain my work later on.

## File Specification
In this Section, I will explain the struture of this Project's folds and files.
Since all source code are updated constantly, some files can not run directly in lastest version, but can run in the version where the file was modified at the last time if you use the time machine of Git.
### Runable files
Files were listed in chronological order
 - main_innaiveData.py: Deal with data '/data/216_shipeng_lanqiu2.csv' containing 6 type label 'stayDribble','runDribble','walk','run','shoot','jump'
 - main_innoiseData.py: Add label 'noise' which exist in '/data/216_ganrao1.csv'. Add data '/data/216_shipeng_lanqiu_test2.csv' for testing in real world sport
 - main_inpasscatchData.py: Add label 'catch','pass' which exist in '/data/253_0909_passcatch.csv', and study in normalization & standarization. Robust normalization is better than other.
 - maininPCA.py: Study in PCA. Normal PCA outperformances the others. PCA with whiten, KernalPCA and PCA using robust normalized data without center are inferior. But in kernalPCA, KNN really benefit from cosine kernal.

	Q: Why center the data before PCA? Spacically when the robust normalization already center the data.
 
 	A: Because the covariance need co-increase or co-decrease according to upright center.
   
	
  	The history of development, there might be some problems when run↑
    
	Up to data and can run without problem ↓
	
 - main_inMultiWind.py: Study in extracting feature using multiplt level windows, that is the model not only extracts feature from a 100 length window, but also from a 200 length window with a step 2.
 - main_only_shootpass.py: Test the Linear model using shoot & pass & catch data. In this test, we can see the robustness for discriminating shooting and passing
 - test_a_file.py: Can read any csv data file and predict it using trained model. It relies on the trained model which should be consistent in feature dimensionality.
 - directlyUseFeature.py: Can read a series of feature files to train the model. Don't need to extract feature from sensor data again. It can be used to train a model, when feature already extracted in other platform(e.g. extracetd in MATLAB)

### Lib files
Files supporting runable file.
 - readData.py: Read data from csv files and preprocessing the sensor data, then return normalized & unnormalized data.
 - splitData.py: According to the type of data (i.e. continuous and discrete activity), to split the data, then return the start point of the window of a data.
 - visualizeStartPointandSeqs.py: To verify the effectness splitter by visualizing the strat points of spliteData.py's return. 
 - extractFeature.py: Extract feature according to the start points in time domain and frequency domain but without m_up feature leading my feature dimensionality is 162. 
   - Using multi-window, it returns 324 dim feature when window level=2. Notice the start point of multi-window should shift to the center of window so that the different level windows can stack like pyramid.
   - I have tested the data which be extracted whether need be normalized instead of zooming in same scalar(i.e. div by 2055). Experiment shows normalized data leads better result than zooming in same scalar.
 - processingFeature.py: Process the extracted feature, include normalize and PCA.
   - Normalize feature using :
   		1. z-score with 0-free degree
   		2. z-score with 1-free degree
   		3. minmax normalization
   		4. robust normalization (Quartile range)
   - PCA feature using:
   		1. normal PCA
   		2. PCA with whiten
   		3. PCA with robust center and scalar (descript in maininPCA.py)
   		4. kernal PCA
 - classification.py: Define the Ensemble learning model and the interface of: 
   - TraininAllClassifiers: Train and test in trainning & testing dataset.
   - save_classifiers, load_classifiers: Save and load the trained model.
   - PrediectinAllClassifiers: Predict data in all trained models and catch the result of all models.
   - CrossValidateClassifiers: Cross-validate all model in trainning and testing dataset.
   - ModethePredict: Capture the mode across the result of all models to give a unified predict result.
 - visualizePredictResult.py: Visualize the original data and predict result, of course can visualize the predict result only.
 - utils.py: Save one or a list of pandas.DataFrame into folds '/intermediadata', this utils can be used to save some intermedia data like extracted feature for saving time.
 - visualizeNormalizeCompare.py: A script should be run after a runable file(main_inXXX.py) running twice in different configuration, then this script will plot the result under the different configuration for comparing.

## Usage
Run the runable file in python2.7.

## TODO
 - Raw sensor data whether need standardization should be discussed, sometime standardization is better than not.
 - PCA can be 25 or lower dimension, e.g. 15, in which case result has't obviously decreased.
 - Co-train to gain data in a semi-supervised learning manner.
