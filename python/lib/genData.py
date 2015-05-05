#!/usr/bin/python

import sys, os, csv, random, time, datetime
sys.path.append('.')
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
from sets import Set

def chkBeginIntervalTime(begin_time, frequency):
    "This function check if the next interval is in future"
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

def genControlInfo(hname, dname, iname, inum, snap_id, start_time, begin_time, end_time, output_dir):
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
   
    o_fname_incl_path = os.path.join(output_dir, o_fname)
    output_file = open( o_fname_incl_path, 'w' )
    output_file.write( '<?xml version="1.0"?>' )
    output_file.write( ElementTree.tostring( ROWSET ) )
    output_file.close()

def getFileName(hname, dname, iname, colltype, snap_id):
    o_fname = "%s.%s.%s.%s.%s" %(hname, dname, iname, colltype, snap_id)
    return o_fname

if __name__ == "__main__":

    print chkBeginIntervalTime('01-MAR-2015 06:00:00',900)

    print getNewIntervalTime('01-MAR-2015 06:00:00',60*100)

    genControlInfo('GB-LD-0001','PGBEQD01','PGBEQI01','1','3451','01-MAR-2015 06:00:00','15-MAR-2015 15:00:00','15-MAR-2015 16:00:00','/Users/bipul/python/out')

    print getFileName('GB-LD-0001','PGBEQD01','PGBEQI01','IOSTAT',3451)
