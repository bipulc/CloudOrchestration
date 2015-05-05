#!/usr/bin/python

import cx_Oracle

con = cx_Oracle.connect('loadgen','loadgen','CAPMAN')
print con.version
cur=con.cursor()
cur.callproc("load_tab_proc",[200])
cur.close()
con.close()
