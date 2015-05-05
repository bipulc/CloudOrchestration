#!/usr/bin/python

import logging

def t_logsetting(logfile, loglevel):

    logging.basicConfig(level=loglevel,
                        format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=logfile,
                        filemode='a')

def t_log(logmessage):
    logging.info(logmessage)

def t_readidenfile(fname):
    "This function reads identity file and return password"
    try:
       fin=open(fname, 'r')
    except:
       (type, detail) = sys.exc_info()[:2]
       print "\n*** %s: %s %s ***" % (conffile, type, detail)
    password = fin.readline()
    fin.close()
    return password


if __name__ == "__main__":

    l_logfile='/tmp/pythontest.log'
    l_loglevel=logging.INFO
    
    t_logsetting(l_logfile, l_loglevel)
    
    t_log('A DEBUG MESSAGE')
    t_log('An Error Message')
    t_log('A Warning  Message')
    x=t_readidenfile('/Users/bipul/python/etc/password')
    print x
