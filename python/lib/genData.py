#!/usr/bin/python

import sys, os, csv, random, time, datetime
sys.path.append('.')
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
from sets import Set

def chkBeginIntervalTime(begin_time, frequency):
    "This function check if the next interval is in future"
    #print "Frequncey = %s" %frequency
    bt_format = datetime.datetime.strptime(begin_time,'%d-%b-%Y %H:%M:%S')
    nextInterval = bt_format + datetime.timedelta(minutes = frequency)
    if nextInterval < datetime.datetime.now():
       return 'Y' 
    else:
       return 'N'

def getNewIntervalTime(begin_time, frequency):
    "This function returns the next Begin Interval Time"
    bt_format = datetime.datetime.strptime(begin_time,'%d-%b-%Y %H:%M:%S')
    nextInterval = bt_format + datetime.timedelta(minutes = frequency)
    return datetime.datetime.strftime(nextInterval, '%d-%b-%Y %H:%M:%S')

def genControlInfo(hname, dname, iname, inum, snap_id, start_time, begin_time, end_time, frequency, output_dir):
    "This function generates control XML file for a database instance"
    o_fname = "%s.%s.%s.%s.%s" %(hname, dname, iname, 'CONTROL', snap_id)
    ROWSET = Element ( 'ROWSET' )
    ROW = SubElement( ROWSET, 'ROW' )
    x = SubElement( ROW, 'HOST_NAME' )
    x.text = hname
    x = SubElement( ROW, 'DATABSE_NAME' )
    x.text = dname
    x = SubElement( ROW, 'INSTANCE_NAME' )
    x.text = iname
    x = SubElement( ROW, 'INSTANCE_NUMBER' )
    x.text = inum
    x = SubElement( ROW, 'SNAP_ID' )
    x.text = snap_id
    x = SubElement( ROW, 'BEGIN_INTERVAL_TIME' )
    x.text = begin_time
    x = SubElement( ROW, 'END_INTERVAL_TIME' )
    x.text = end_time
    x = SubElement( ROW, 'STARTUP_TIME' )
    x.text = start_time
    x = SubElement( ROW, 'FREQUENCY' )
    x.text = str(frequency)
       
    o_fname_incl_path = os.path.join(output_dir, o_fname)
    output_file = open( o_fname_incl_path, 'w' )
    output_file.write( '<?xml version="1.0"?>' )
    output_file.write( ElementTree.tostring( ROWSET ) )
    output_file.close()

def getFileName(hname, dname, iname, colltype, snap_id):
    "This function generates output filename for element and collection type"
    o_fname = "%s.%s.%s.%s.%s" %(hname, dname, iname, colltype, snap_id)
    return o_fname

def chkRestart(m,n):
    "This function checks if an instance has been restarted"
    if random.randint(m,n) == 13:
       return True
    else:
       return False
       
def newStartTime(begin_time,freq):
    "This function creates a new start time for an instance."
    n_start_time = datetime.datetime.strptime(begin_time,'%d-%b-%Y %H:%M:%S') + datetime.timedelta(minutes = random.randint(1,freq-1))
    return datetime.datetime.strftime(n_start_time,'%d-%b-%Y %H:%M:%S')

    
if __name__ == "__main__":

    print chkBeginIntervalTime('01-MAR-2015 06:00:00',900)

    print getNewIntervalTime('01-MAR-2015 06:00:00',int(60*5))

    genControlInfo('GB-LD-0001','PGBEQD01','PGBEQI01','1','3451','01-MAR-2015 06:00:00','15-MAR-2015 15:00:00','15-MAR-2015 16:00:00',60,'/Users/bipul/python/out')

    print getFileName('GB-LD-0001','PGBEQD01','PGBEQI01','IOSTAT',3451)
    
    for i in range(1,5):
       cr = chkRestart(1,20)
    
       if cr:
          print 'Run %s -- instance restarted' %i
       else:
          print 'Run %s -- instance not restarted' %i

    print newStartTime('01-MAR-2015 06:00:00',60)