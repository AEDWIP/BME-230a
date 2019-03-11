# AWS set
- running on local mac is too slow
- tried moving to google driver and colab. colab only supports 11G ram
- share/save code via git hub


list all files that have ever been under git
```
$ git log --pretty=format: --name-status | cut -f2- | sort -u
```

0. prevent mac from shutting down
   * <span style="color:red"> settings -> power adapter -> prevent computer from sleeping automatically when display is off</span>
   * set a reminder to turn this off at end of the day
   

1. log into AWS
   * use the Amazon details in onePassword, userid andy@SantaCruzIntegration.com
   * select the EC2 console -> instances.You will see our sci webserver
   * see secure notes in onePassword
     + SCI AWS
     + SantaCruzIntegration Website
     + Amazon EC2 ?SCI?
       * https://console.aws.amazon.com/ec2/v2/home?region=us-west-1#KeyPairs:
2. ec2 console -> instance -> launch
   * image Deep Learning AMI (Ubuntu) Version 21.2 - ami-0f627d6558d18ecfa
     + has tensorflow-1.12
     + configured with NVIDIA CUDA, cuDNN, NCCL, Intel MKL-DNN, Docker & NVIDIA-Docker
   * instance type
     + general purpose m5d.2xlarge 8 vpc 32GB memory 300 SSD
     + security SCI_webServer
       * allows ssh and http:80
   * select key pair "SCI_AWS
     - this is the same one we use for newsci in ~/.ssh/config
     
3. ssh
```
$ ssh -i ~/.ssh/SCI_AWS.pem ubuntu@ec2-public-IP
```

4. activate the
for TensorFlow(+Keras2) with Python3 (CUDA 9.0 and Intel MKL-DNN) ___________________________ source activate tensorflow_p36

```
$  source activate tensorflow_p36
```

4. set up our clone

```
(tensorflow_p36) ubuntu@ip-172-31-8-231:~$ git clone https://github.com/AEDWIP/BME-230a.git
(tensorflow_p36) ubuntu@ip-172-31-8-231:~$ cd BME-230a
(tensorflow_p36) ubuntu@ip-172-31-8-231:~/BME-230a$ git fetch origin
(tensorflow_p36) ubuntu@ip-172-31-8-231:~/BME-230a$ git checkout -b AEDWIP_brand --track origin/AEDWIP_brand
```

5. copy the data and model files.
* did not want to put them in github. they are big
* use scp
  ```
  $ cd ~/andrewdavidson/workSpace/UCSC/BME-230a/project
  $ scp -r user@your.server.example.com:/path/to/foo /home/user/Desktop
  $ scp -r user@your.server.example.com:/path/to/foo /home/user/Desktop
  
  $ time scp  -i ~/.ssh/SCI_AWS.pem ubuntu@ec2-public-IP -r ./models ubuntu@ec2-13-52-78-122.us-west-1.compute.amazonaws.com:/home/ubuntu/BME-230a 
  ```

6. SCP is really slow, create an S3 bucket
   * log into s3 console
   * create in same region as ec2 instance
   * bucket bme-230a.santacruzintegration.com
   
7. aws zapper provides integration with google driver. probably faster to move data this way
   * https://zapier.com/apps/amazon-ec2/integrations/google-drive
   
   
   shareable link to data
   https://drive.google.com/open?id=1OfRTmEkB0bhs2F8lp1ejtREGlqZevije
   
     
https://support.cloudhq.net/how-to-sync-amazon-s3-and-google-drive/

https://linuxconfig.org/google-drive-on-ubuntu-18-04-bionic-beaver-linux
Google Drive via google-drive-ocamlfuse PPA

```
(tensorflow_p36) ubuntu@ip-172-31-8-231:~$ sudo add-apt-repository ppa:alessandro-strada/ppa
(tensorflow_p36) ubuntu@ip-172-31-8-231:~$ sudo apt install google-drive-ocamlfuse
E: Unable to locate package google-drive-ocamlfuse

```

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


# oka you can not easily move data from google driver
- run robs notebook
 https://github.com/rcurrie/tumornormal.git


 ssh -i ~/.ssh/SCI_AWS.pem -o ServerAliveInterval=120 -N -f -L localhost:8889:localhost:8888  ubuntu@ec2-52-53-176-249.us-west-1.compute.amazonaws.com
 
 
 # can not run all of Rob's notebook
 $ time scp -i ~/.ssh/SCI_AWS.pem ./tcga_target_gtex.h5 ubuntu@ec2-52-53-176-249.us-west-1.compute.amazonaws.com:/home/ubuntu


ubuntu@ip-172-31-15-92:~$ aws s3 cp googleDrive/GD_BME230a/project/data s3://bme-230a.santacruzintegration.com --recursive


upload failed: googleDrive/GD_BME230a/project/data/TcgaTargetGTEX_phenotype.txt.gz to s3://bme-230a.santacruzintegration.com/TcgaTargetGTEX_phenotype.txt.gz Unable to locate credentials


ubuntu@ip-172-31-15-92:~$ aws s3 cp tcga_target_gtex.h5 s3://bme-230a.santacruzintegration.com/tcga_target_gtex.h5


https://support.infinitewp.com/support/solutions/articles/212258-where-are-my-amazon-s3-credentials-

create a user "aed"
see onepassword aws SCI userId:aed


figure out how to use aws.aed.credentials.csv 
export AWS_ACCESS_KEY_ID=AKIAISTKGQ336ZZXW3EQ
ubuntu@ip-172-31-15-92:~$ export AWS_SECRET_ACCESS_KEY=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

```
ubuntu@ip-172-31-15-92:~$ aws s3 cp t s3://bme-230a.santacruzintegration.com/t
upload: ./t to s3://bme-230a.santacruzintegration.com/t  
```

```
ubuntu@ip-172-31-15-92:~$ aws s3 cp googleDrive/GD_BME230a/project/data s3://bme-230a.santacruzintegration.com --recursive
upload: googleDrive/GD_BME230a/project/data/TcgaTargetGTEX_phenotype.txt.gz to s3://bme-230a.santacruzintegration.com/TcgaTargetGTEX_phenotype.txt.gz
```

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

```
ubuntu@ip-172-31-15-92:~$ aws s3 cp tcga_target_gtex.h5 s3://bme-230a.santacruzintegration.com/tcga_target_gtex.h5
```


add EBS pandas can not read file from s3, must be local

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
git config user.name andy@santaCruzIntegration.com
