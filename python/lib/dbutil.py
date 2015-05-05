#!/usr/bin/python

# Module for database utilities

import cx_Oracle

def t_createconn(uname, passwd, service):
    "This funtion creates a database connection using input params"
    conn = cx_Oracle.connect(uname, passwd, service)
    return conn
   

def t_testconn(con):
    "This function tests connection"
    print con.version


def t_closeconn(con):
    "This function closes connection"
    con.close()


def t_createcursor(con):
    "This function creates a cursor"
    return con.cursor()


if __name__ == "__main__":

   uname='loadgen'
   passwd='loadgen'
   service='capman'

   c=t_createconn(uname, passwd, service)
   t_testconn(c)
   cur=t_createcursor(c)
   cur.callproc("load_tab_proc",[200]) 
   cur.close()
   t_closeconn(c)
