#!/usr/bin/python
import sys, os, csv, random, argparse
sys.path.append('../lib')
import helper, logging, genData
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
from sets import Set

# This script will need to be rewritten for multi threading

parser = argparse.ArgumentParser()
parser.add_argument("-t", type=str, help="topology file")
parser.add_argument("-m", type=str, help="metrics file")
parser.add_argument("-l", type=str, help="logfile")
parser.add_argument("-n", type=int, help="number of files to generate")
parser.add_argument("-odir", type=str, help="output directory")
args = parser.parse_args()


topology_file = csv.DictReader(open(args.t))
output_dir=args.odir
fh = open(args.m, 'rb')
counter_file = csv.DictReader(fh)
logfile=args.l
colltype_unq = Set()

# Set logging and print name of logfile to check
loglevel="INFO"
nloglevel =getattr(logging, loglevel, None)
helper.t_logsetting(logfile, nloglevel)
print ("\nMain: execution information in logfile %s " %logfile)
print ("Starting performance data generation ...")
helper.t_log('Starting performance data generation ...')

# Function to generate value of counter
# Takes three argument, Minval, Maxval, Counter Type and optionally prev value

# Build a unique list of Collection Type
for colltype in counter_file:
    colltype_unq.add(colltype["COLLTYPE"])

# Reset the file handle for metrics to the begining again
fh.seek(0)
ThreadNum = 0


# Interate over all elements in the topology.
for row in topology_file:
    hname = row["HOSTNAME"]
    dname = row["DBNAME"]
    iname = row["INSNAME"]
    inum = row["INSNUMBER"]
    snapid = row["SNAPID"]
    inssize =row["INSSIZE"]
    start_time = row["STARTUPTIME"]
    begin_time = row["BEGIN_INT_TIME"]
    freq = row["FREQUENCY"]

    for i in range(1,args.n):
        print ("i -- %s" %i)
        print ("Begin Interval Time -- %s   --  Frequncy -- %s" %(begin_time,freq))
       
        # Check if the begin_interval_time is in future
        nextTimeInPast = genData.chkBeginIntervalTime(begin_time, int(freq*i))
    
        if nextTimeInPast == 'Y':
     
           helper.t_log('Thread| ' + str(ThreadNum) + ':Processing Hostname ' + hname + ' instance size ' + inssize)
           n_begin_time = genData.getNewIntervalTime(begin_time, int(freq*i))
           n_end_time = genData.getNewIntervalTime(n_begin_time, int(freq))
           n_snap_id = int(snapid) + i

           # Function to generate Generic control info for an element
           genData.genControlInfo(hname, dname, iname, inum, str(n_snap_id), start_time, n_begin_time, n_end_time, output_dir)
    
           # Get list of all CollType from counter file
  
           for x in colltype_unq:
              o_fname = genData.getFileName(hname,dname,iname,x,n_snap_id)
	      # o_fname = "%s.%s.%s.%s.%s" %(hname, dname, iname, x, snapid)

	      # Ensure that the file pointer is at the begining of the file
	      fh.seek(0)

              # Initialize Dictionary to hold CounterValues
              CounterCurrVal = {}

              for metrics in counter_file:
                 if inssize == metrics["INSSIZE"] and metrics["COLLTYPE"] == x:
                    helper.t_log('Thread| ' + str(ThreadNum) + ': Collection Type ' +metrics["COLLTYPE"] + ' - Counter Name ' + metrics["COUNTERNAME"] + ' - Min Value ' + str(metrics["MINVAL"]) + ' - Max Value ' + str(metrics["MAXVAL"]))
           
                    # Call random number gen function to generate a value for 
                    # counter between MIN and MAX value
	       
	            CountVal = random.randint(int(metrics["MINVAL"]),int(metrics["MAXVAL"]))
               
                    #print "Value of Counter %s is %s" % (metrics["COUNTERNAME"], CountVal)

                    # print CounterCurrVal
	            # Store the countername, value in a dictionary object
                    # and use it for printing XML file
                    CounterCurrVal[metrics["COUNTERNAME"]] = CountVal

              ROWSET = Element( 'ROWSET' )
              ROW = SubElement( ROWSET, 'ROW' )
 
              for CntCurrVal in CounterCurrVal.items():
              #print "CounterCurrVal : CounterName - %s  CounterVal - %s " % (CntCurrVal[0], CntCurrVal[1])
                 x = SubElement( ROW, CntCurrVal[0] )
                 x.text = str(CntCurrVal[1])
           o_fname_incl_path = os.path.join(output_dir, o_fname)
           output_file = open( o_fname_incl_path, 'w' )
           output_file.write( '<?xml version="1.0"?>' )
           output_file.write( ElementTree.tostring( ROWSET ) )
           output_file.close()

    # Update topology file
    #updatetoplogy(hname, dname, iname, snapid, start_time, begin_time, end_time)

    print "... %s" %hname
print "Performance data generated ..."
print "Output files in directory %s" %output_dir
print "\n"
