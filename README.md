# READ ME
Author: Andrew E. Davidson
aedavids@ucsc.edu

## virtual env 
- tensorflow requires python 3.6
- use requirements.txt
  * <span style="color:red">WE NEEDED to down grade some packages, numpy, keras</span>
- has numpy, keras, tensorflow, matplotlib, and juypter. 
- <span style="color:red">BY DEFAULT YOU WILL GET A BAD VERSION OF NUMPY</span>
  * we got numpy 1.16.1
  * we can not load Y
    + Y = pd.read_hdf(dataFile, "labels")
    + [https://github.com/pandas-dev/pandas/issues/24839](https://github.com/pandas-dev/pandas/issues/24839)
  * work around
    +  pip install numpy==1.15.4
```
$ source ~/workSpace/pythonEnv/BME_230a_py3.6/bin/activate
```

## starting juypter notebook
```
(BME_230a_py3.6) $ pwd
/Users/andrewdavidson/workSpace/UCSC/BME-230a/project
(BME_230a_py3.6) $ juypter notebook
```

## Notebook run order and overview
1. rcurrie-tumornormal/ingest.ipynb
    * downloads data if needed
    * clean and transforms
        + convert ENSEMBL gene ids to Hugo
    * writes data/tcga_target_gtex.h5
2. simpleModel.ipynb
    * loads data/tcga_target_gtex.h5
    * trains tumor normal binary classifier
        + saves model if models/logisticRegressionlogisticRegressionTumorNormal does not exist
    * stats
      ```
      train
      Loss    : 0.0101
      Accuracy: 0.9993

      test
      Loss    : 0.0226
      Accuracy: 0.9958
      
      # confusion matrix
      [[1709   11]
      [   5 2101]]
      
      False positive rate: (predicting tumor while normal) 0.006395348837209302
      False negative rate: (predicting normal while tumor) 0.0023741690408357074      
      ```
    
     

## our local git repo
- tensorFlowForDeepLearning is a clone of the orely example code- see [Adding New Submodules](https://stackoverflow.com/a/4962025/4586180)
- set up:
  * after git init
```
(BME_230a_py3.6) $ pwd
/Users/andrewdavidson/workSpace/UCSC/BME-230a/project
(BME_230a_py3.6) $ git submodule add https://github.com/matroid/dlwithtf.git tensorFlowForDeepLearning
Cloning into '/Users/andrewdavidson/workSpace/UCSC/BME-230a/project/tensorFlowForDeepLearning'...
```


## paricially conneced layers
- [google search](https://www.google.com/search?q=tensorflow+partially+connected+layer&oq=tensorflow+partially&aqs=chrome.0.0j69i57j0l3j69i64.6294j0j7&sourceid=chrome&ie=UTF-8)
- [stack overflow add mask to tf.graph](https://stackoverflow.com/a/53855389/4586180)
-[LSTM inspired gates to control flow](https://medium.com/jim-fleming/highway-networks-with-tensorflow-1e6dfa667daa)
- [tensorflow sparse](https://www.tensorflow.org/api_docs/python/tf/sparse/SparseTensor)
- [tf.sparse.to_indicator](https://www.tensorflow.org/api_docs/python/tf/sparse/to_indicator)


## TumorNormal repos
- rcurrie
```
$ pwd
/Users/andrewdavidson/workSpace/UCSC/BME-230a/project
$ git clone https://github.com/rcurrie/tumornormal.git ./rcurrie-tumornormal
```

- ingest.ipynb
  * Toil expression is labeled using Ensembl gene ids vs. Treehouse which uses Hugo
  * down loads the data sets
    + tcga_target_gtex_expressionDF: samples=60498 genes=19260
    + example gene (col) names
      ^ GTEX-1117F-0226-SM-5GZZ7
      ^ TCGA-ZR-A9CJ-01
    + each row has a "sampleId" ???
      ^ example ENSG00000000003.14
      ^ I think this is the Ensemble gene id
      ^ psudo selection: [ENSG00000242268.2, GTEX-1117F-0226-SM-5GZZ7] = -9.9658
  * data wrangling
    + convert Ensembl gene ids to Hugo 
    + psudo selection:   [RP11-368I23.2,     GTEX-1117F-0226-SM-5GZZ7] = -9.9658
    + [Gene: RP11-368I23.2 ENSG00000242268](http://grch37.ensembl.org/Homo_sapiens/Gene/Summary?g=ENSG00000242268;r=3:168621154-168639784;t=ENST00000484765)
  
  * col
  * Genotype-Tissue Expression (GTEx) 
    + [E-MTAB-5214 - RNA-seq from 53 human tissue samples from the Genotype-Tissue Expression (GTEx) Project](https://www.ebi.ac.uk/arrayexpress/experiments/E-MTAB-5214/samples/?s_sortby=col_1&s_sortorder=descending) 
- train.ipynb
  * keras binary classifier
  * example of how to load/read the tidy data set. 
- multiclass.ipynb
  * better example 
  
- pathways.ipynb
  *  17810 gene sets in the Molecular Signatures Database (MSigDB) 
     + [http://software.broadinstitute.org/gsea/msigdb/collections.jsp](http://software.broadinstitute.org/gsea/msigdb/collections.jsp])
     + [kegg pathway database](https://www.genome.jp/kegg/pathway.html)
     + [PATHWAY: hsa05216 hyroid cancer - Homo sapiens (human)](https://www.genome.jp/dbget-bin/www_bget?pathway+hsa05216)
     + [Thyroid cancer - Homo sapiens (human)](https://www.genome.jp/kegg-bin/show_pathway?org_name=hsa&mapno=05216&mapscale=&show_description=show)
  * see section Primary Site Classification w/Per Pathway Sub-Network Input Layer

- our old TumorNormal repo
```
$ pwd
/Users/andrewdavidson/workSpace/UCSC/mlCoop/tumornormal
$ gb -v
  master  971a15c [origin/master] # merge of evalLogisticRegression branch
* pathway 2d501d4 [origin/master: ahead 22] Merge remote-tracking branch 'origin/master' into pathway
$ git remote -v
origin	https://github.com/AEDWIP/tumornormal.git (fetch)
origin	https://github.com/AEDWIP/tumornormal.git (push)
upstream	https://github.com/rcurrie/tumornormal.git (fetch)
upstream	https://github.com/rcurrie/tumornormal.git (push)
```


# NOTES
- data from 3 data sets 
  * [https://xenabrowser.net/datapages/?host=https://toil.xenahubs.net](https://xenabrowser.net/datapages/?host=https://toil.xenahubs.net)
    + The Cancer Genome Atlas (TCGA)
    + Genotype-Tissue Expression (GTEx)
    + Therapeutically Applicable Research To Generate Effective Treatments (TARGET)

# overview of pathway information




# SAVE pages about autonomus AI and FDA
- [https://aaii.ucsc.edu/2019/02/11/scml-meeting-february-20-2019/](https://aaii.ucsc.edu/2019/02/11/scml-meeting-february-20-2019/)
- [https://www.nature.com/articles/s41591-018-0300-7](https://www.nature.com/articles/s41591-018-0300-7)
- [https://www.eyediagnosis.net/](https://www.eyediagnosis.net/)
- [https://www.fda.gov/NewsEvents/Newsroom/PressAnnouncements/ucm604357.htm](https://www.fda.gov/NewsEvents/Newsroom/PressAnnouncements/ucm604357.htm)
- [https://www.newswire.com/news/pmwc-2019-silicon-valley-has-grown-to-worlds-largest-precision-20758265](https://www.newswire.com/news/pmwc-2019-silicon-valley-has-grown-to-worlds-largest-precision-20758265)
