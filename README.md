##Managaing Database Cloud Services using REST API

Oracle Database Cloud Service offers REST APIs to create and manage service instances. These APIs are described in detail in [Oracle Cloud Documentation] (http://docs.oracle.com/cloud/latest/dbcs_dbaas/CSDBR/toc.htm) . 

The Cloud Orchestration framework is a set of python script embedding the REST APIs. The purpose of this project is

1.  Demonstrate the ease of managing Oracle Database Cloud Service via REST APIs.
2.  A sample code for integration with existing workflow.

The code has been developed using Python 2.7.10 on OS X 10.11, but should work on any OS with Python 2.6 or 2.7 installation.

####Directory Structure

Top level directory - CloudOrchestrator
  
| Sub Directory | Description | Files |
|---------------|-------------|-------|
|bin            | Main script directory | opc-dbcs.py|
|etc            | Reference files such as json and web-services configuration |opc-dbcs-ws.ref,createdbcs_vm_img.json |
|lib            | Python sript for modules and helper scripts|opchelper.py|
|log            | Log file from execuetion of ops-dbcs.py script|

####Installation 

1.  Download source code from [release page] (https://github.com/bipulc/CloudOrchestration/releases/tag/0.1).
2.  Untar (or unzip) in any directory on your computer.
3.  Install certificate file as per instruction from [cURL Documentation site] (https://curl.haxx.se/docs/caextract.html). Its as easy as download the cacert.pem file and store in a directory ( e.g. I have stored the cacert.pem file in /Users/bipul/keys directory)
4.  Change directory to bin, and run ./opc-dbcs.py -h to verify installation.

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

opc-dbcs.py provides the following functionality from command line using web services.

1.  Build Oracle Database Cloud Service (Single Instance and RAC).
2.  View status of database service(s) in an indentity domain.
3.  Scale UP and Scale DOWN CPU and Memory allocated to a Database Cloud Service.
4.  Allocate more storage to Database Cloud Service.
5.  Manage Lifecycle (Stop, Start and Restart) Database Cloud Service.

Output of the execution is written to standard output (screen) as well as to a log file for auditing and review if necessary.

####High Level Flowchart

The diagram below shows high level flow of the program. Validation of arguments and parsing of input parameters are carried out in  script opc-dbcs.py. Library file opchelper.py implements module for invocation of the web services with appropriate verb. A job id is returned to the calling script, if the request is accepted by Oracle Public Cloud ( http return code 202). opc-dbcs.py script then monitors the job until completion. It writes log of the execution on the screen and in the specified log file.

![Image of Flowchart](https://github.com/bipulc/CloudOrchestration/blob/master/OPC-DBCS-WsOpsInterface.001.jpeg)

####Prerequisite

1.  Oracle Cloud Account with DBCS subscription
2.  Python 2.6 or 2.7
3.  cacert.pem file as per installation instructions.

####Example



