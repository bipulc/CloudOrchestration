#!/usr/bin/python

from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

# <ROWSET>
ROWSET = Element( 'ROWSET' )

# <ROWSET>/<ROW>
ROW = SubElement( ROWSET, 'ROW' )

# <ROWSET>/<ROW>/COUNTER

l_c1 = 'PHYRDS'

x = SubElement( ROW, l_c1 )
x.text = str(935)

l_c2 = 'READTIM'

x = SubElement( ROW, l_c2 )
x.text = '258'

output_file = open( 'membership.xml', 'w' )
output_file.write( '<?xml version="1.0"?>' )
output_file.write( ElementTree.tostring( ROWSET ) )
output_file.close()
