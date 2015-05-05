#!/usr/bin/python

###################################################################################
# Script: load_gen.py
# Purpose: Generate Load in an Oracle database
# Author: Bipul Kumar
# Date: 13 July 2014. 
###################################################################################

import sys, getopt, os
sys.path.append('../lib')
import helper, logging
import dbutil

def usage():
   "This function prints usage of the script on screen"
   print 'usage: load_gen.py -c <config file>'

def setConfFile(argv):
   "This function sets name of config file to conffile variable"

   global conffile
   try:
      opts, args = getopt.getopt(argv,"h:c:",["conf="])
   except getopt.GetoptError:
      usage()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         usage()
         sys.exit()
      elif opt in ("-c", "--conf"):
         conffile = arg


def parseConf(conffile, confdict = []):
   "This function parses config file and load into a dictionary"

   try:
      fin = open(conffile, 'r')
   except:
      (type, detail) = sys.exc_info()[:2]
      print "\n*** %s: %s %s ***" % (conffile, type, detail)
   # print "\n*** Contents of", conffile, "***"

   # Print the file, with line numbers.
   lno = 1
   while 1:
      line = fin.readline()
      if not line: break;
      # print '%3d: %-s' % (lno, line[:-1])
      if not line.startswith("#"):
        key, value = line.split('=')
        confdict[key.strip()] = value.strip()
        lno = lno +1
   fin.close()

def validateConfig(confdict):
   "This function validates variables passed through config file"
   if confdict.has_key('THREADS'):
      l_numth = confdict['THREADS']
      helper.t_log('Thread| Main: Number of Thread Requested - ' + str(l_numth))
   else:
      helper.t_log('Thread| Main: 0 Thread Requested. Load_gen will run in single thread mode')
      
   if confdict.has_key('REPO_DB'):
      helper.t_log('Thread| Main: Repository Database ' + confdict['REPO_DB'])
   else:
      helper.t_log('Thread| Main: Repository Database not specified. Aborting ...')
      sys.exit(1)

   if confdict.has_key('USERNAME'):
      helper.t_log('Thread| Main: Repository Database User Name ' + confdict['USERNAME'])
   else:
      helper.t_log('Thread| Main: Repository Database User Name not specified. Aborting ...')
      sys.exit(1)

   if confdict.has_key('IDENFILE'):
      l_idenfile = confdict['IDENFILE']
      if os.path.isfile(l_idenfile) and os.access(l_idenfile, os.R_OK):
         helper.t_log('Thread| Main: Identity file ' + l_idenfile + ' exists and readable')
         password = helper.t_readidenfile(l_idenfile).strip()
         # helper.t_log('Thread| Main: Password ' + password)
      else:
         helper.t_log('Thread| Main: Identity file ' + l_idenfile + ' does not exist or is not readable. Aborting ...')
         sys.exit(1)
   else:
      helper.t_log('Thread| Main: Repository user identity file not specified. Aborting ...')
      sys.exit(1)

   if confdict.has_key('SQLDIR'):
      l_sqldir = confdict['SQLDIR']
      if os.path.isdir(l_sqldir):
         helper.t_log('Thread| Main: SQLDIR ' + l_sqldir + ' exists ');
      else:
         helper.t_log('Thread| Main: SQLDIR ' + l_sqldir + ' does not exist. No SQL file to execute ...')
   else:
      helper.t_log('Thread| Main: SQLDIR parameter not specified. No SQL file to execute ...')

   if confdict.has_key('TIMEOUT'):
      l_timeout = confdict['TIMEOUT']
      helper.t_log('Thread| Main: Timeout set to ' +  l_timeout)
   else:
      helper.t_log('Thread| Main: Timeout parameter not set')


if __name__ == "__main__":

   print
   # Set Deafult Log file and Logging Level. Could be overwritten in config file
   l_deflogfile='/tmp/load_gen.log'
   l_defloglevel='INFO'

   # Store Script Name
   l_scrname = os.path.basename(__file__)

   print 'Starting load generator script: ', l_scrname
   print 'Starting Thread Main:'

   #Global Valriables to store config file name and config data

   conffile=''
   confdict = {}
   
   # Parse CMD argument and Get Config Filename
   setConfFile(sys.argv[1:])
   print 'Thread| Main: Config File: ', conffile 
  
   # Parge content of config file and store in dictionary
   parseConf(conffile, confdict)

   # Check if Log file and Leg Level is set, otehrwise set to default 
   if confdict.has_key('LOGFILE'):
      l_logfile = confdict['LOGFILE']
   else:
      l_logfile = l_deflogfile

   print 'Thread| Main: Logfile : ', l_logfile

   if confdict.has_key('LOGLEVEL'):
      l_loglevel = confdict['LOGLEVEL']
   else:
      l_loglevel = l_defloglevel

   print 'Thread| Main: Loglevel : ',l_loglevel
   
   # Get numeric value for Log Level
   l_nloglevel = getattr(logging, l_loglevel.upper(), None)

   helper.t_logsetting(l_logfile, l_nloglevel)
   print ("Thread| Main: check logfile %s for further information..." % l_logfile )
   helper.t_log('Starting load gen ...')
   helper.t_log('Thread| Main: Logfile and Loglevel set')
   
   validateConfig(confdict)
   
   # Call Db functions
   
   l_idenfile = confdict['IDENFILE']
   password = helper.t_readidenfile(l_idenfile).strip()
   l_conn = dbutil.t_createconn(confdict['USERNAME'], password, confdict['REPO_DB'])
   dbutil.t_testconn(l_conn)
   l_dbcursor = dbutil.t_createcursor(l_conn)
   l_dbcursor.callproc("load_tab_proc",[200])
   l_dbcursor.close()
   dbutil.t_closeconn(l_conn) 
