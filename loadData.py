'''
loadData:

Created on Mar 5, 2019
@author: andrewdavidson aedavids@ucsc.edu

public functions:
    loadTumorNormalData()
    loadKerasModel(modelName)
    saveKerasModel(modelName)
'''

from keras.utils import np_utils
import numpy as np
import os
import pandas as pd
import sys

# fix random seed for reproducibility
theMeaningOfLife = 42
np.random.seed(theMeaningOfLife)


_sourceDataFile = "data/tcga_target_gtex.h5"            
_tumorNormalFile = "data/logisticRegressionTumorNormal.h5" 


################################################################################        
def loadTumorNormalData(projectDir):
    '''
     aedwip

    arguments:
        projectDir: root of project
        
    TODO: do not recompute cache data to disk
    '''
    sourceDataFilePath = "{}/{}".format(projectDir, _sourceDataFile)
    print("sourceDataFilePath:{}".format(sourceDataFilePath))
    store = pd.HDFStore(sourceDataFilePath, mode="r")
    #print("{} source store.info():{}".format(_sourceDataFile, store.info()))
    #print("{} store.keys():{}".format(_sourceDataFile, store.keys()))
     
    # Load training set
    X = pd.read_hdf(sourceDataFilePath, "expression")
    Y = pd.read_hdf(sourceDataFilePath, "labels")
 
    # Convert tumor_normal  into numerical values 
    from sklearn.preprocessing import LabelEncoder
     
    encoder = LabelEncoder()
    Y["tumor_normal_value"] = pd.Series(encoder.fit_transform(Y["tumor_normal"]), index=Y.index)
    #Y[["tumor_normal","tumor_normal_value"]].head(3)
     
    # Split into stratified training and test sets based on classes (i.e. tissue type) so that we have equal
    # proportions of each tissue type in the train and test sets
    from sklearn.model_selection import StratifiedShuffleSplit
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=theMeaningOfLife)
    for train_index, test_index in split.split(X.values, Y["tumor_normal_value"]):
        X_train, X_test = X.values[train_index], X.values[test_index]
        y_train, y_test = Y["tumor_normal_value"][train_index], \
                            Y["tumor_normal_value"][test_index]  
     
    #print("AEDWIP X_train.shape:{}".format(X_train.shape))
    #print("AEDWIP X.shape:{} len(X.columns):{}".format(X.shape, len(X.columns)))
    
    # X_train and X_test are numpy arrays
    XTrainDF = pd.DataFrame(X_train, columns=X.columns)
    XTestDF = pd.DataFrame(X_test, columns=X.columns)
    
    # y_train and y_test are pandas series
    #yTrainDF = pd.DataFrame(y_train, columns=["tumor_normal_value"])
    yTrainDF = pd.DataFrame(y_train, columns=["tumor_normal_value"])
    yTrainDF.head(3)
    yTestDF = pd.DataFrame(y_test, columns=["tumor_normal_value"])
    #return (X_train, y_train, X_test, y_test)
    #return (XTrainDF, yTrainDF, XTestDF, yTestDF)
    return (XTrainDF, y_train, XTestDF, y_test)

################################################################################        
def loadCancerDiseaseTypeTidyDataSet(projectDir):
    '''
    preformes the following steps
    * load projectDir/data/tcga_target_gtex.h5
    * remove all 'Normal' cases
    * encodes 'disease' string labels 
    * creates one-hot reprsentation of disease values
    * calls StratifiedShuffleSplit to split into  80/20 train/test set
    
    ref: 
        diseaseTypeClassifier.ipynb
    
        https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html
    
    return (hugoIds, diseaseLabelEncoder, XTrainNumpy, yTrainNumpy, XTestNumpy, yTestNumpy)
        hugoIds, a numpy array of strings. These are hugo column labels for the feature columns
        
        diseaseLabelEncoder:
            an instance of sklearn.preprocessing.LabelEncoder. use 
            inverse_transform(disease_value) to recover original string label
            
        XTrainNumpy.shape: (8424, 58581) XTestNumpy.shape: (2106, 58581)
        yTrainNumpy.shape: (8424, 39)    yTestNumpy.shape: (2106, 39)
        
        y shapes explained
            the first column is the encode disease type of type int
            the remain columns are the one-hot encoding
     
    TODO do not recompute cache data to disk
    '''
    sourceDataFilePath = "{}/{}".format(projectDir, _sourceDataFile)
    print("sourceDataFilePath:{}".format(sourceDataFilePath))
    store = pd.HDFStore(sourceDataFilePath, mode="r")
    #print("{} source store.info():{}".format(_sourceDataFile, store.info()))
    #print("{} store.keys():{}".format(_sourceDataFile, store.keys()))
     
    # Load training set
    XDF = pd.read_hdf(sourceDataFilePath, "expression")
    yDF = pd.read_hdf(sourceDataFilePath, "labels")
    
    # fetch the column names
    hugoIds = XDF.columns.values
    
    # remove normal cases
    yTumorRows = yDF['tumor_normal'] != 'Normal'        
    yTumorDF = yDF.loc[yTumorRows, ['disease', 'tumor_normal']]

    yTumorDF = yDF[yTumorRows]
    yDF = yTumorDF
    yTumorDF = None # free memory

    XTumorDF = XDF[yTumorRows]
    XDF = XTumorDF
    XTumorDF = None # free memory

    # Convert tumor_normal  into numerical values 
    from sklearn.preprocessing import LabelEncoder
    
    # Convert disease  into numerical values 
    # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html
    diseaseLabelEncoder = LabelEncoder()
    yDF["disease_value"] = pd.Series(diseaseLabelEncoder.fit_transform(yDF["disease"]), index=yDF.index)
    
    # create one hot encodings
    oneHots = np_utils.to_categorical(yDF["disease_value"])
    #print(type(oneHots))
    #print(oneHots.shape)

    diseaseValues = yDF["disease_value"].values.reshape(yDF.shape[0],-1)
    #print(type(diseaseValues))
    #print(diseaseValues.shape)

    yOneHots = np.append(diseaseValues, oneHots, axis=1)
    
    # Split into stratified training and test sets based on classes (i.e. disease type) 
    # so that we have equal proportions of each disease type in the train and test sets
  
    from sklearn.model_selection import StratifiedShuffleSplit
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=theMeaningOfLife)
    for train_index, test_index in split.split(XDF.values, yDF["disease_value"]):
        XTrainNumpy = XDF.values[train_index]
        XTestNumpy  =  XDF.values[test_index]
        yTrainNumpy = yOneHots[train_index]
        yTestNumpy  = yOneHots[test_index]
        
    # pandas series values attribute create numpy arrays with shapes that are under specified
    # E.G. yTestNumpy.shape: (3826,) .this causes a lot of bugs in other packages
    # reshape(n,-1) causes reshape to set the last value
    yTrainNumpy = np.reshape(yTrainNumpy,(yTrainNumpy.shape[0], -1))
    yTestNumpy  = np.reshape( yTestNumpy, (yTestNumpy.shape[0], -1))   
    
    return (hugoIds, diseaseLabelEncoder, XTrainNumpy, yTrainNumpy, XTestNumpy, yTestNumpy)
    

