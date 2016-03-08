#!/usr/bin/python
'''Python Wrapper for OPC DBCS RESTFul APIs
# ---  TO DO List --- #
  1. Dependencies between arguments, e.g. -d is only valid with -o BUILD 
  2. Raise error and exit if operation requested does not have an entry in web services ref file 
  3. Replace web service reference file from csv to json
  4. Standarize output to log file and to screen
  5. Catch KeyboardInterrupt Exception
  
'''

import sys, os, csv, argparse, getpass, requests, time
sys.path.append('../lib')
import opchelper, logging

parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str, help="identity domain")
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-o", type=str, help="operations {BUILD|DELETE|SCALE|STOP|START|RESTART|VIEW|VIEW_JOB")
parser.add_argument("-w", type=str, help="web service ref file")
parser.add_argument("-l", type=str, help="logfile (fullpath)")
parser.add_argument("-c", type=str, help="certificate file (fullpath)")
parser.add_argument("-d", type=str, help="json file for creating dbcs service", nargs='?')
parser.add_argument("-n", type=str, help="dbcs service name", nargs='?')
parser.add_argument("-s", type=str, help="compute shape", nargs='?')
parser.add_argument("-j", type=str, help="job number", nargs='?')
args = parser.parse_args()

# Prompt for password input and store in a variable
password = getpass.getpass('Identity Domain Password:')

iden_domain = args.i
username = args.u
operation = args.o
wsref_file = args.w
cert_file = args.c
log_file = args.l
service_name = args.n
compute_shape = args.s
dbcs_def_file = args.d

# Set logging and print name of logfile to check
loglevel="INFO"
nloglevel =getattr(logging, loglevel, None)
opchelper.t_logsetting(log_file, nloglevel)
print ("\nMain: execution information in logfile %s " %log_file)
#print ("Main: DBCS Operation Request: %s " %operation)
opchelper.t_log('\n')
opchelper.t_log('Thread| Main : ' + 'DBCS Operation Request: ' + str(operation))



# Read Web Service Reference file into a dictionary

ws_dict = csv.DictReader(open(wsref_file))


for row in ws_dict:
    l_ops = row["OPERATION"]
    l_method = row["METHOD"]
    l_rest_endpoint = row["REST_ENDPOINT"]
    if l_ops == operation:
        opchelper.t_log('Thread| Main : ' + 'Method - ' +  str(l_method))
        opchelper.t_log('Thread| Main : ' + 'Rest Endpoint - ' +  str(l_rest_endpoint))

        job_id = opchelper.t_exec(operation, iden_domain, l_method, l_rest_endpoint, cert_file, username, password, service_name, compute_shape, dbcs_def_file)
        print "%s: Job Id : %s" % (time.ctime(time.time()), job_id)
        if job_id > 0 :
            while True:
               job_output = opchelper.t_viewjob (operation, iden_domain, l_rest_endpoint, cert_file, username, password, job_id)
               if job_output:
                  print "%s: Job status %s" % (time.ctime(time.time()), job_output['job_status'])
                  print "%s: Message %s" % (time.ctime(time.time()), job_output['message'])
                  print
                  if job_output['job_status'] in ('Succeeded','Failed'):
                     print "%s: Service status %s" % (time.ctime(time.time()), job_output['status'])
                     break
               time.sleep(30)

