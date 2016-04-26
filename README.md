##Managaing Database Cloud Services using REST API

Oracle Database Cloud Service offers REST APIs to create and manage service instances. These APIs are described in detail in [Oracle Cloud Documentation] (http://docs.oracle.com/cloud/latest/dbcs_dbaas/CSDBR/toc.htm) . 

The Cloud Orchestration framework is a set of python script embedding the REST APIs. The purpose of this project is

1.  Demonstrate the ease of managing Oracle Database Cloud Service via REST APIs.
2.  A sample code for integration with existing workflow.

The code has been developed using Python 2.7.10 on OS X 10.11, but should work on any OS with Python 2.6 or 2.7 installation.

####Directory Structure

CloudOrchestrator -> Top-level 
  - /bin -> main script directory
  - /etc -> json files and web-services reference file
  - /lib -> python script for modules / helper script
  - /log -> execution log file
  
####Installation 

1.  Download script CloudOrchestrator.tar from [Github Page] (https://github.com/bipulc/CloudOrchestration/blob/master/CloudOrchestrator.tar).
2.  Untar the file into a directory named CloudOrchestrator (or any other name you like).
3.  Install certificate file as per instruction from [cURL Documentation site] (https://curl.haxx.se/docs/caextract.html). Its as easy as download the cacert.pem file and store in a directory ( e.g. I have stored the cacert.pem file in /Users/bipul/keys directory)

####Usage

```
$./opc-dbcs.py -h
usage: opc-dbcs.py [-h] [-i I] [-u U] [-o O] [-w W] [-l L] [-c C] [-d [D]]
                   [-n [N]] [-s [S]] [-j [J]]

optional arguments:
  -h, --help  show this help message and exit
  -i I        identity domain
  -u U        username
  -o O        operations {BUILD|DELETE|SCALE|STOP|START|RESTART|VIEW|VIEW_JOB
  -w W        web service ref file
  -l L        logfile (fullpath)
  -c C        certificate file (fullpath)
  -d [D]      json file for creating dbcs service
  -n [N]      dbcs service name
  -s [S]      compute shape
  -j [J]      job number
$

```

####Features

####Example



