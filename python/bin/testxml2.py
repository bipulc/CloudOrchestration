#!/usr/bin/python

import sys
sys.path.append('../lib')
from etbuilder import et, E

l_hname = 'OraCloud'

ROWSET = E.ROWSET(
   E.ROW(
      E.HOST_NAME(l_hname),
      E.DATABASE_NAME('ORACLOUD'),
      E.SNAP_ID(34)
   ),
   E.ROW(
      E.HOST_NAME(l_hname),
      E.DATABASE_NAME('ORACLOUD'),
      E.SNAP_ID(35)
   )
)

print 'XML for host ', l_hname
print  et.tostring(ROWSET, pretty_print=True)

# Reset host name
l_hname = 'oem12c'

ROWSET = E.ROWSET(
   E.ROW(
      E.HOST_NAME(l_hname),
      E.DATABASE_NAME('ORACLOUD'),
      E.SNAP_ID(34)
   ),
   E.ROW(
      E.HOST_NAME(l_hname),
      E.DATABASE_NAME('ORACLOUD'),
      E.SNAP_ID(35)
   )
)
print 'XML for host ', l_hname
print  et.tostring(ROWSET, pretty_print=True)

# Reset host name
l_hname = 'GBL0101D'
l_dname = 'GBL0101D01'
l_snapid = 34
c_htag = 'HOST_NAME'
c_dtag = 'DATABASE_NAME'
c_stag = 'SNAP_ID'

ROWSET = E.ROWSET(
   E.ROW(
      E.c_htag(l_hname),
      E.DATABASE_NAME('ORACLOUD'),
      E.SNAP_ID(34)
   )
)
print 'XML for host ', l_hname
print  et.tostring(ROWSET, pretty_print=True)
