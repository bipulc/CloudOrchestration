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
parser.add_argument("-n", type=int, help="number of files to generate", nargs='?', const=2, default=2)
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

# Local Variables
# First and Last number used for instance restart evaluation. (randomly simulate instance restart situation)
# If a random number between crfirst and crlast is 13 then instance has been restarted

crfirst = 1
crlast = 20

# Build a unique list of Collection Type
for colltype in counter_file:
    colltype_unq.add(colltype["COLLTYPE"])

# Reset the file handle for metrics to the begining again
fh.seek(0)
ThreadNum = 0

# Generate a filename to write new topology file
n_topology_file = genData.newTopologyFname(args.t)
print "New Topology File - %s" %n_topology_file
fh_n_topology = open(n_topology_file, 'w+')
t_writer = csv.writer(fh_n_topology)
# Write header of topology file
genData.updatetoplogy(t_writer,'HOSTNAME','DBNAME','INSNAME','INSNUMBER','INSSIZE','STARTUPTIME','SNAPID','BEGIN_INT_TIME','FREQUENCY')

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
        # print ("i -- %s" %i)
        # print ("Begin Interval Time -- %s   --  Frequncy -- %s" %(begin_time,freq))
       
        # Check if the begin_interval_time is in future
        nextTimeInPast = genData.chkBeginIntervalTime(begin_time, int(freq)*i)
    
        if nextTimeInPast == 'Y':
     
           helper.t_log('Thread| ' + str(ThreadNum) + ':Processing Hostname ' + hname + ' instance size ' + inssize)
           n_begin_time = genData.getNewIntervalTime(begin_time, int(freq)*i)
           n_end_time = genData.getNewIntervalTime(n_begin_time, int(freq))
           n_snap_id = int(snapid) + i

           # Check if the element has been restarted during last observation period
           
           restart_flag = False
           if genData.chkRestart(crfirst, crlast):
              start_time = genData.newStartTime(n_begin_time, int(freq))
              # Set a restart flag, to be used later in the code
              restart_flag = True
              print 'Snap Id - %s Hname - %s New start time - %s' %(n_snap_id, hname, start_time)
           
           # Function to generate Generic control info for an element
           genData.genControlInfo(hname, dname, iname, inum, str(n_snap_id), str(start_time), n_begin_time, n_end_time, freq, output_dir)
    
           # Get list of all CollType from counter file
  
           for x in colltype_unq:
              o_fname = genData.getFileName(hname,dname,iname,x,n_snap_id)

	      # Ensure that the file pointer for the metrics file is at the begining of the file
	      fh.seek(0)

              # Initialize Dictionary to hold CounterValues
              CounterCurrVal = {}

              for metrics in counter_file:
                 if inssize == metrics["INSSIZE"] and metrics["COLLTYPE"] == x:
                    helper.t_log('Thread| ' + str(ThreadNum) + ': Collection Type ' +metrics["COLLTYPE"] + ' - Counter Name ' + metrics["COUNTERNAME"] + ' - Min Value ' + str(metrics["MINVAL"]) + ' - Max Value ' + str(metrics["MAXVAL"]))
   
                    # Check if the Counter is a cumulative counter and the instance has not been restarted, read the previous perf data file
                    if metrics["COUNTERTYPE"] == 'C' and not restart_flag:
                       p_fname = genData.getPrevFileName(output_dir,hname,dname,iname,x,n_snap_id)
                       if p_fname is not None:
                          # Get the value of Counter and add to random number generated between Min and Max
                          CountVal = random.randint(int(metrics["MINVAL"]),int(metrics["MAXVAL"])) + genData.getPrevCountVal(p_fname, metrics["COUNTERNAME"])
                          CounterCurrVal[metrics["COUNTERNAME"]] = CountVal
                       else:
                          # Previous perf datafile not found
                          CountVal = random.randint(int(metrics["MINVAL"]),int(metrics["MAXVAL"]))
                          CounterCurrVal[metrics["COUNTERNAME"]] = CountVal
                    else:   
                       # Call random number gen function to generate a value for counter between MIN and MAX value
	               CountVal = random.randint(int(metrics["MINVAL"]),int(metrics["MAXVAL"]))
                       CounterCurrVal[metrics["COUNTERNAME"]] = CountVal
               
                    # print "Value of Counter %s is %s" % (metrics["COUNTERNAME"], CountVal)
                    # print CounterCurrVal
	            # Store the countername, value in a dictionary object and use it for printing XML file

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
    genData.updatetoplogy(t_writer, hname, dname, iname, inum, inssize, start_time, n_snap_id, n_begin_time, freq)

    print "... %s" %hname
# Close all files
fh_n_topology.close()
fh.close()

# rename new topology file to ensure its used in next run
os.rename(n_topology_file, args.t)

print "Performance data generated ..."
print "Output files in directory %s" %output_dir
print "\n"
