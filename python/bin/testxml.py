#!/usr/bin/python
import lxml.etree
import lxml.builder    

E = lxml.builder.ElementMaker()
ROWSET = E.ROWSET
ROW = E.ROW
FIELD1 = E.field1
FIELD2 = E.field2

the_doc = ROWSET(
        ROW(
            FIELD1('some value1', name='blah'),
            FIELD2('some value2', name='asdfasd'),
            )   
        )   

print lxml.etree.tostring(the_doc, pretty_print=True)
