# AWS set up
- running on local mac is too slow
- tried moving to google driver and colab. colab only supports 11G ram
- google driver backup & sync is very very slow. It corpted my data files

## Overview
* share code via github
* run jupyter on ec2 instance using ssh tunnel to connect to browser on mac
* store data sets in S3
* store data on EBS
  * notebook can not load data from S3
  * want data to be close so read is fast
  
## Instructions and Notes


list all files that have ever been under git
```
$ git log --pretty=format: --name-status | cut -f2- | sort -u
```

1. prevent mac from shutting down
   * <span style="color:red"> settings -> power adapter -> prevent computer from sleeping automatically when display is off</span>
   * set a reminder to turn this off at end of the day
   * we want to be able to walk away from long running process with out breaking connections
   

2. log into AWS
   * use the Amazon details in onePassword, userid andy@SantaCruzIntegration.com
   * select the EC2 console -> instances.You will see our sci webserver
   * see secure notes in onePassword
     + SCI AWS
     + SantaCruzIntegration Website
     + Amazon EC2 ?SCI?
       * https://console.aws.amazon.com/ec2/v2/home?region=us-west-1#KeyPairs:
      
      
3. ec2 console -> instance -> launch
   * image Deep Learning AMI (Ubuntu) Version 21.2 - ami-0f627d6558d18ecfa
     + has tensorflow-1.12
     + configured with NVIDIA CUDA, cuDNN, NCCL, Intel MKL-DNN, Docker & NVIDIA-Docker
   * instance type
     + general purpose m5d.2xlarge 8 vpc 32GB memory 300 SSD
     + security SCI_webServer
       * allows ssh and http:80
   * select key pair "SCI_AWS
     - this is the same one we use for newsci in ~/.ssh/config
   * created a launch template <span style="color:red">BME-230a-launchTemplate</span>
     
     
4. ssh
   ```
   $ ssh -i ~/.ssh/SCI_AWS.pem ubuntu@ec2-public-IP
   ```

5. start the required environment with the framework 
   * for TensorFlow(+Keras2) with Python3 (CUDA 9.0 and Intel MKL-DNN) ___________________________ source activate tensorflow_p36

    ```
    $  source activate tensorflow_p36
    ```

6. set up our local git repo

    ```
    (tensorflow_p36) ubuntu@ip-172-31-8-231:~$ git clone https://github.com/AEDWIP/BME-230a.git
    (tensorflow_p36) ubuntu@ip-172-31-8-231:~$ cd BME-230a
    (tensorflow_p36) ubuntu@ip-172-31-8-231:~/BME-230a$ git fetch origin
    (tensorflow_p36) ubuntu@ip-172-31-8-231:~/BME-230a$ git checkout -b AEDWIP_branch --track origin/AEDWIP_branch
    ```

    * to be able to push back to origin
      ```
      git config user.name andy@santaCruzIntegration.com
      ```
    * when we push will be prompted for name and password
      + use credentials for github in onepassword

7. copy the data and model files.
   * did not want to put them in github. they are big
   * use scp
     ```
     $ cd ~/andrewdavidson/workSpace/UCSC/BME-230a/project  
     $ time scp  -i ~/.ssh/SCI_AWS.pem ubuntu@ec2-public-IP -r ./models ubuntu@ec2-13-52-78-122.us-west-1.compute.amazonaws.com:/home/ubuntu/BME-230a 
     ```

8. SCP is really slow, create an S3 bucket
   * log into s3 console
   * create in same region as ec2 instance
   * bucket <span style="color:red">bme-230a.santacruzintegration.com</span>
   * more step required see bellow (create user, credentials, aws cli, ...)

9. set up python and juypter on ec2
   * pip instalal --user Keras=2.1.6
     + by default got a newer version. 
     + newer version can not save and restore models
     + by default juypter server runns on port 8888
     
10. starting juypter server and connecting to mac
    * on ec2 
      ```
      $ jupyter notebook
      ```
      
    * you will need token see juypter server log files
      + it easier to copy the entire url and just change the port from 8888 to 8889

    * on mac open ssh tunnel
      ```
       ssh -i ~/.ssh/SCI_AWS.pem -o ServerAliveInterval=120 -N -f -L localhost:8889:localhost:8888  ubuntu@ec2-52-53-176-249.us-west-1.compute.amazonaws.com
      ```
      
    * on mac start brower 
    * open terminal on mac
    * open url from jupyter log file <span style="color:red">make sure you change the port to 8889</span>

11. tried to run robs notebook to down load data
    * this failed. wound up using scp to transfer data files from mac
    * https://github.com/rcurrie/tumornormal.git

 
## can not run all of Rob's notebook scp data files from mac
a. on mac
    ```
    $ time scp -i ~/.ssh/SCI_AWS.pem ./tcga_target_gtex.h5 ubuntu@ec2-52-53-176-249.us-west-1.compute.amazonaws.com:/home/ubuntu
    ```

b. on ec2 move to s3
    * see additianon notes
    ```
    ubuntu@ip-172-31-15-92:~$ aws s3 cp tcga_target_gtex.h5 s3://bme-230a.santacruzintegration.com/tcga_target_gtex.h5    
    ```


    * https://support.infinitewp.com/support/solutions/articles/212258-where-are-my-amazon-s3-credentials-
    * create a user "andy"
    * see onepassword aws SCI userId:andy
    * figure out how to use aws.andy.credentials.csv 
    * export AWS_ACCESS_KEY_ID=AEDWIP
    * ubuntu@ip-172-31-15-92:~$ export AWS_SECRET_ACCESS_KEY=AEDWIP

    ```
    ubuntu@ip-172-31-15-92:~$ aws s3 ls s3://bme-230a.santacruzintegration.com
    2019-03-11 00:25:26     135753 TcgaTargetGTEX_phenotype.txt.gz
    2019-03-11 00:24:37        125 t
    2019-03-11 00:25:26        260 testFileTransfer.txt
    2019-03-11 00:25:27       1024 treehouse.h5
    2019-03-11 00:25:27          0 treehouse_public_samples_clinical_metadata.2017-09-11.tsv.gz
    2019-03-11 00:25:27          0 treehouse_public_samples_unique_hugo_log2_tpm_plus_1.2017-09-11.tsv.gz
    ubuntu@ip-172-31-15-92:~$ 
    ```


# add EBS pandas can not read file from s3, must be local
* used console to create a 100G volume and attach to our instance
* the devices not formated or mounted
* log on format
* mount
* if we stop and start instance we may have to remount the EBS volumne
  + the mount point /bme-230a-ebs should already exist
    - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html
      ```
      root@ip-172-31-15-92:/home/ubuntu# ls -ld /bme-230a-ebs
      drwxr-xr-x 2 root root 4096 Mar 11 01:20 /bme-230a-ebs
      ```
      
  + find the attached volume that has not been attached yet
    * nvme0n1 is not mounted and is 100 G this must be it
    ```
    root@ip-172-31-15-92:/home/ubuntu# lsblk
    NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
    loop0         7:0    0  17.9M  1 loop /snap/amazon-ssm-agent/1068
    loop1         7:1    0    91M  1 loop /snap/core/6350
    loop2         7:2    0    18M  1 loop /snap/amazon-ssm-agent/930
    loop3         7:3    0  89.5M  1 loop /snap/core/6130
    loop4         7:4    0  16.5M  1 loop /snap/amazon-ssm-agent/784
    loop5         7:5    0    91M  1 loop /snap/core/6405
    nvme0n1     259:2    0    75G  0 disk 
    └─nvme0n1p1 259:3    0    75G  0 part /
    nvme1n1     259:1    0   100G  0 disk 
    nvme2n1     259:0    0 279.4G  0 disk     
    ```
    
  + mount the volume sudo mount /dev/xvdf /data
    ```
    root@ip-172-31-15-92:/home/ubuntu# mount /dev/nvme1n1 /bme-230a-ebs
root@ip-172-31-15-92:/home/ubuntu# ls /bme-230a-ebs/
data  models  t
    ```

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AmazonEBS.html

https://www.youtube.com/watch?v=DS1nF1WBGKk

https://aws.amazon.com/ebs/getting-started/

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-creating-volume.html


BME-230a-project  volume id: vol-026c8e33988a1475b


https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-attaching-volume.html

you can attach to running instance using ec2 console or aws cli

https://docs.aws.amazon.com/cli/latest/reference/ec2/attach-volume.html

make volum avalible to unix users
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html

ubuntu@ip-172-31-15-92:~$ aws ec2 describe-volumes --region us-west-1


     {
            "VolumeId": "vol-026c8e33988a1475b",
            "Encrypted": false,
            "State": "in-use",
            "Iops": 300,
            "Attachments": [
                {
                    "VolumeId": "vol-026c8e33988a1475b",
                    "State": "attached",
                    "Device": "/dev/sdf",
                    "DeleteOnTermination": false,
                    "AttachTime": "2019-03-11T01:03:37.000Z",
                    "InstanceId": "i-01b819e0862d1dfc0"
                }
            ],
            "Size": 100,
            "Tags": [
                {
                    "Value": "bme-230a-EBS",
                    "Key": "name"
                },
                {
                    "Value": "bme-230a-ebs",
                    "Key": "Name"
                }
            ],
            "CreateTime": "2019-03-11T01:02:23.216Z",
            "SnapshotId": "",
            "VolumeType": "gp2",
            "AvailabilityZone": "us-west-1c"
        },


did not work git config --global user.name andy@SantaCruzIntegration.com


# Note on how to access google driver from ubuntu
* using google driver is hard and data transfer rate is really bad
   
https://www.techrepublic.com/article/how-to-mount-your-google-drive-on-linux-with-google-drive-ocamlfuse/

(tensorflow_p36) ubuntu@ip-172-31-8-231:~$ sudo add-apt-repository ppa:alessandro-strada/ppa
(tensorflow_p36) ubuntu@ip-172-31-8-231:~$ sudo apt-get update
(tensorflow_p36) ubuntu@ip-172-31-8-231:~$ sudo apt install google-drive-ocamlfuse

 mkdir ~/google-drive
 google-drive-ocamlfuse ~/google-drive
 
 
 https://stackoverflow.com/a/39333278/4586180
 
 
 recipe for headless
 https://olgabotvinnik.com/blog/googledrive-ubuntu/
 ref: https://github.com/astrada/google-drive-ocamlfuse
 sudo add-apt-repository ppa:alessandro-strada/ppa
 sudo apt update && sudo apt install google-drive-ocamlfuse
 
 see direction for using wizard to get google api crediential
 we created a new project "my-project-234121
 OAuth 2.0 client IDs name "Driver API Quickstart"
 google-drive-ocamlfuse ~/googledrive -headless
 
client id   212201324120-jeod9t9kc1qk5iv1kn20t4h09c2r1b8u.apps.googleusercontent.com
client secrete  MLeJs8VVpwI0ZgkjSH0JhaCG
 
 $ scp  -i ~/.ssh/SCI_AWS.pem ubuntu@ec2-public-IP  ./client_secret.json ubuntu@ec2-13-52-78-122.us-west-1.compute.amazonaws.com:/home/ubuntu

in the json file you will find keys "client_id" and "client_secret"

$  google-drive-ocamlfuse ~/googleDrive -headless -id 212201324120-jeod9t9kc1qk5iv1kn20t4h09c2r1b8u.apps.googleusercontent.com -secret MLeJs8VVpwI0ZgkjSH0JhaCG

you get a url open it on mac to authorize
