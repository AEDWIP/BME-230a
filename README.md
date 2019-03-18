# A comparison of known cancer causing genes with those identified by a classifier trained on gene expression data.

- BME 230A class project winter 2019
- Andrew E. Davidson
- [aedavids@ucsc.edu](mailto:aedavids@edu?subject=SimpleModel.ipynb)

Note for best viewing experience open links on github. [https://github.com/AEDWIP/BME-230a](https://github.com/AEDWIP/BME-230a)  GitHub will automatically render the jupyter notebook files into html. If you experience a rendering problem click on the git hub reload button. Save as PDF sometimes clips plots and puts page breaks in strange places

## Installation notes
- clone this repo
- download the required data set
  * you can find a copy at s3://bme-230a.santacruzintegration.com/tcga_target_gtex.h5
  * or run [Rob Curries' ingest notebook](https://github.com/rcurrie/tumornormal/blob/master/ingest.ipynb)

## Table of Contents:
* [BME-230a-2019-paper-aedavids@ucsc.edu.ipynb  notebook](./BME-230a-2019-paper-aedavids@ucsc.edu.ipynb)
  + final class report. 
* [simpleModelEvaluation.ipynb notebook](./simpleModelEvaluation.ipynb)
  + logistic regresion model evaluation
* [simpleModel.ipynb notebook](./simpleModel.ipynb)
  + data exploration, and logistic regression  model creation 
* [diseaseTypeClassifierEval.ipynb notebook](./diseaseTypeClassifierEval.ipynb)
  + disease type mulit-classier evaluation
* [diseaseTypeClassifier.ipynb notebook](./diseaseTypeClassifier.ipynb)
  + data exploration and softmax mult-classifer model creation
* [dimensionaltyReducedDiseaseTypeClassifier.ipynb notebook](./dimensionaltyReducedDiseaseTypeClassifier.ipynb)
  * uses PCA to move from a high to low dimension traning space
* [awsSetUpNotes.md](./awsSetUpNotes.md)
  + poorly written notes about how to spin up a large machine in AWS
  + file is in markdown format. If you do not have a markdown viewer you can easily read this file using a text editor. The format looks like ascii email
  
