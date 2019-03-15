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

# ################################################################################        
# def _AEDWIP_loadCleanWriteTumorNormalData():
#     '''
#     this does not work, loosing to much time debugging H5
#     
#     1. loads data/tcga_target_gtex.h5
#     2. encodes Y["tumor_normal_value"]
#     3. StratifiedShuffleSplit on Y["tumor_normal_value"]
#     4. save to data/tumorNormal.h5
#     '''
#     store = pd.HDFStore(_sourceDataFile, mode="r")
#     print("{} source store.info():{}".format(_sourceDataFile, store.info()))
#     print("{} store.keys():{}".format(_sourceDataFile, store.keys()))
#     
#     # Load training set
#     X = pd.read_hdf(_sourceDataFile, "expression")
#     Y = pd.read_hdf(_sourceDataFile, "labels")
# 
#     # Convert tumor_normal  into numerical values 
#     from sklearn.preprocessing import LabelEncoder
#     
#     encoder = LabelEncoder()
#     Y["tumor_normal_value"] = pd.Series(encoder.fit_transform(Y["tumor_normal"]), index=Y.index)
#     #Y[["tumor_normal","tumor_normal_value"]].head(3)
#     
#     # Split into stratified training and test sets based on classes (i.e. tissue type) so that we have equal
#     # proportions of each tissue type in the train and test sets
#     from sklearn.model_selection import StratifiedShuffleSplit
#     split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=theMeaningOfLife)
#     for train_index, test_index in split.split(X.values, Y["tumor_normal_value"]):
#         X_train, X_test = X.values[train_index], X.values[test_index]
#         y_train, y_test = Y["tumor_normal_value"][train_index], \
#                             Y["tumor_normal_value"][test_index]  
#                             
#     print("AEDWIP type(X_train):{}".format(type(X_train)))
#     print("AEDWIP type(y_train):{}".format(type(y_train)))                             
#     print("AEDWIP X_train.shape:{}".format(X_train.shape))
#     print("AEDWIP y_train.shape:{}".format(y_train.shape)) 
#     sys.stdout.flush() 
#     
#     X_train = pd.DataFrame(data=X_train, columns=X.columns)
#     y_train = pd.DataFrame(data=y_train, columns=["tumor_normal_value"])
#     X_test  = pd.DataFrame(data=X_test,  columns=X.columns)
#     y_test  = pd.DataFrame(data=y_test,  columns=["tumor_normal_value"])
#     
#     print("\n convert to pandas")
#     print("AEDWIP type(X_train):{}".format(type(X_train)))
#     print("AEDWIP type(y_train):{}".format(type(y_train)))                             
#     print("AEDWIP X_train.shape:{}".format(X_train.shape))
#     print("AEDWIP y_train.shape:{}".format(y_train.shape)) 
#     sys.stdout.flush()     
#     
#     # numpy.ndarray' object has no attribute 'dtypes'                      
# #     print("AEDWIP X_train.dtypes:{}".format(X_train.dtypes))
# #     print("AEDWIP y_train.dtypes:{}".format(y_train.dtypes))
#     # Export h5 format files
#     with pd.HDFStore(_tumorNormalFile, "w") as store:
#         # https://riptutorial.com/pandas/example/9812/using-hdfstore
#         store.append("X_train", X_train)
#         print("stored XT")
#         store.append("y_train", y_train)
#         print("stored yt")
#         store.append("X_test",  X_test)
#         print ("stored xtest")
#         store.append("y_test",  y_test)
#         print("stored ytest")
#         # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.T.html
# #         store["X_train"] = X_train #.T.sort_index(axis="columns")
# #         store["y_train"] = y_train        
# #         store["X_test"] = X_test #.T.sort_index(axis="columns")
# #         store["y_test"] = y_test


################################################################################        
# def _AEDWIP_loadCleanWriteTumorNormalData():
#     '''
#     this does not work, loosing to much time debugging H5
    
#     1. loads data/tcga_target_gtex.h5
#     2. encodes Y["tumor_normal_value"]
#     3. StratifiedShuffleSplit on Y["tumor_normal_value"]
#     4. save to data/tumorNormal.h5
#     '''
#     store = pd.HDFStore(_sourceDataFile, mode="r")
#     print("{} source store.info():{}".format(_sourceDataFile, store.info()))
#     print("{} store.keys():{}".format(_sourceDataFile, store.keys()))
    
#     # Load training set
#     X = pd.read_hdf(_sourceDataFile, "expression")
#     Y = pd.read_hdf(_sourceDataFile, "labels")

#     # Convert tumor_normal  into numerical values 
#     from sklearn.preprocessing import LabelEncoder
    
#     encoder = LabelEncoder()
#     Y["tumor_normal_value"] = pd.Series(encoder.fit_transform(Y["tumor_normal"]), index=Y.index)
#     #Y[["tumor_normal","tumor_normal_value"]].head(3)
    
#     # Split into stratified training and test sets based on classes (i.e. tissue type) so that we have equal
#     # proportions of each tissue type in the train and test sets
#     from sklearn.model_selection import StratifiedShuffleSplit
#     split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=theMeaningOfLife)
#     for train_index, test_index in split.split(X.values, Y["tumor_normal_value"]):
#         X_train, X_test = X.values[train_index], X.values[test_index]
#         y_train, y_test = Y["tumor_normal_value"][train_index], \
#                             Y["tumor_normal_value"][test_index]  
                            
#     print("AEDWIP type(X_train):{}".format(type(X_train)))
#     print("AEDWIP type(y_train):{}".format(type(y_train)))                             
#     print("AEDWIP X_train.shape:{}".format(X_train.shape))
#     print("AEDWIP y_train.shape:{}".format(y_train.shape)) 
#     sys.stdout.flush() 
    
#     X_train = pd.DataFrame(data=X_train, columns=X.columns)
#     y_train = pd.DataFrame(data=y_train, columns=["tumor_normal_value"])
#     X_test  = pd.DataFrame(data=X_test,  columns=X.columns)
#     y_test  = pd.DataFrame(data=y_test,  columns=["tumor_normal_value"])
    
#     print("\n convert to pandas")
#     print("AEDWIP type(X_train):{}".format(type(X_train)))
#     print("AEDWIP type(y_train):{}".format(type(y_train)))                             
#     print("AEDWIP X_train.shape:{}".format(X_train.shape))
#     print("AEDWIP y_train.shape:{}".format(y_train.shape)) 
#     sys.stdout.flush()     
    
#     # numpy.ndarray' object has no attribute 'dtypes'                      
# #     print("AEDWIP X_train.dtypes:{}".format(X_train.dtypes))
# #     print("AEDWIP y_train.dtypes:{}".format(y_train.dtypes))
#     # Export h5 format files
#     with pd.HDFStore(_tumorNormalFile, "w") as store:
#         # https://riptutorial.com/pandas/example/9812/using-hdfstore
#         store.append("X_train", X_train)
#         print("stored XT")
#         store.append("y_train", y_train)
#         print("stored yt")
#         store.append("X_test",  X_test)
#         print ("stored xtest")
#         store.append("y_test",  y_test)
#         print("stored ytest")
#         # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.T.html
# #         store["X_train"] = X_train #.T.sort_index(axis="columns")
# #         store["y_train"] = y_train        
# #         store["X_test"] = X_test #.T.sort_index(axis="columns")
# #         store["y_test"] = y_test

# ################################################################################        
# def loadTumorNormalData():
#     '''
#         creates data/tumorNormal.h5 if it does not exist
#         
#         returns (X_train, y_train, X_test, y_test)
#     '''
#     if not os.path.isfile(_tumorNormalFile):
#         _loadCleanWriteTumorNormalData()
#     
#     store = pd.HDFStore(_tumorNormalFile, mode="r")
#     print("store.info():{}".format(store.info()))
#     print("store.keys():{}".format(store.keys()))
#     
#     X_train = pd.read_hdf(_sourceDataFile, "X_train")
#     y_train = pd.read_hdf(_sourceDataFile, "y_train")
#     
#     X_test = pd.read_hdf(_sourceDataFile, "X_test")
#     y_test = pd.read_hdf(_sourceDataFile, "y_test")
#     
#     return (X_train, y_train, X_test, y_test)


################################################################################        
def loadTumorNormalData(projectDir):
    '''
     aedwip

    arguments:
        projectDir: root of project
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
    
################################################################################        
def loadKerasModel(modelName):
    '''
    AEDWIP
    
    assumes path ./models/modelName.json and ./models/modelName.h5
    
    returns model
    '''
#     from keras.models import model_from_json
#     modelPath = "./models/{}.json".format(modelName)
#     modelWeightsPath = "./models/{}.h5".format(modelName)
#     print("modelPath:{}".format(modelPath))
#     print("modelWeightsPath:{}".format(modelWeightsPath))
# 
#     # https://machinelearningmastery.com/save-load-keras-deep-learning-models/
#     # load json and create model
# #     with open(modelPath, 'r') as jsonFile:
# #         modelJson = jsonFile.read()
# #         jsonFile.close()
# #         model = model_from_json(modelJson)
# #         # load weights into new model
# #         model.load_weights(modelWeightsPath)
# #         print("Loaded model:{} from disk".format(modelName))
#         
#     jsonFile =  open(modelPath, 'r')      
#     modelJson = jsonFile.read()
#     jsonFile.close()
#     model = model_from_json(modelJson)
#     # load weights into new model
#     model.load_weights(modelWeightsPath)
#     print("Loaded model:{} from disk".format(modelName))
        
    
    return model

# ################################################################################        
# def saveKerasModel(model, modelName):
#     '''
#     AEDWIP
#     
#     assumes path ./models/modelName.json and ./models/modelName.h5
#     
#     returns model
#     '''
#     # save model
#     # https://machinelearningmastery.com/save-load-keras-deep-learning-models/
#     # serialize model to JSON
#     modelPath = "./models/{}.json".format(modelName)
#     modelWeightsPath = "./models/{}.h5".format(modelName)
#     
#     if not os.path.isfile(modelPath) and not os.path.isfile(modelWeightsPath):
#         with open(modelPath, "w") as json_file:
#             modelJson = model.to_json()
#             json_file.write(modelJson)
#         # serialize weights to HDF5
#         model.save_weights(modelWeightsPath)
#         print("Saved model to disk")
#     else:
#         print("ERROR: model was not save. files already exist {} {}".format(modelPath, modelWeightsPath))
#             
