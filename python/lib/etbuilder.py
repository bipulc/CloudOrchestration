"""etbuilder.py: An element builder for lxml.etree
================================================================
    $Revision: 1.55 $  $Date: 2012/08/11 21:44:19 $
================================================================
For documentation, see:
    http://www.nmt.edu/tcc/help/pubs/pylxml/
Borrows heavily from the work of Fredrik Lundh; see:
    http://effbot.org/zone/
"""
#================================================================
# Imports
#----------------------------------------------------------------

from lxml import etree as et
try:
    from functools import partial
except ImportError:
    def partial(func, *args, **keywords):
        def newfunc(*fargs, **fkeywords):
            newkeywords = keywords.copy()
            newkeywords.update(fkeywords)
            return func(*(args + fargs), **newkeywords)
        newfunc.func  =  func
        newfunc.args  =  args
        newfunc.keywords  =  keywords
        return newfunc
# - - -   C L A S S

def CLASS(*names):
    '''Helper function for adding 'class=...' attributes to tags.

      [ names is a list of strings ->
          return a dictionary with one key 'class' and the related
          value the concatenation of (names) with one space between
          them ]
    '''
    return {'class': ' '.join(names)}
# - - -   F O R

def FOR(id):
    '''Helper function for adding 'for=ID' attributes to tags.
    '''
    return {'for': id}
# - - -   s u b E l e m e n t

def subElement(parent, child):
    '''Add a child node to the parent and return the child.

      [ (parent is an Element) and
        (child is an Element with no parent) ->
          parent  :=  parent with child added as its new last child
          return child ]
    '''
    #-- 1 --
    parent.append(child)

    #-- 2 --
    return child
# - - -   a d d T e x t

def addText(node, s):
    '''Add text content to an element.

      [ (node is an Element) and (s is a string) ->
          if node has any children ->
              last child's .tail  +:=  s
          else ->
              node.text +:= s ]
    '''
    #-- 1 --
    if not s:
        return

    #-- 2 --
    if len(node) == 0:
        node.text = (node.text or "") + s
    else:
        lastChild = node[-1]
        lastChild.tail = (lastChild.tail or "") + s
# - - - - -   c l a s s   E l e m e n t M a k e r

class ElementMaker(object):
    '''ElementTree element factory class

      Exports:
        ElementMaker(typeMap=None):
          [ (typeMap is an optional dictionary whose keys are
            type objects T, and each corresponding value is a
            function with calling sequence
              f(elt, item)
            and generic intended function
              [ (elt is an et.Element) and
                (item has type T) ->
                  elt  :=  elt with item added ]) ->
              return a new ElementMaker instance that has
              calling sequence
                E(*p, **kw)
              and intended function
                [ p[0] exists and is a str ->
                    return a new et.Element instance whose name
                    is p[0], and remaining elements of p become
                    string content of that element (for types
                    str, unicode, and int) or attributes (for
                    type dict, and members of kw) or children
                    (for type et.Element), plus additional
                    handling from typeMap if it is provided ]
              and allows arbitrary method calls of the form
                E.tag(*p, **kw)
              with intended function
                [ return a new et.Element instance whose name
                  is (tag), and elements of p and kw have
                  the same effects as E(*(p[1:]), **kw) ]
    '''
# - - -   E l e m e n t M a k e r . _ _ i n i t _ _

    def __init__(self, typeMap=None):
        '''Constructor for the ElementMaker factory class.
        '''
        #-- 1 --
        # [ if typeMap is None ->
        #     self.__typeMap  :=  a new, empty dictionary
        #   else ->
        #     self.__typeMap  :=  a copy of typeMap ]
        if typeMap is None:
            self.__typeMap  =  {}
        else:
            self.__typeMap  =  typeMap.copy()
        #-- 2 --
        # [ self.__typeMap[str], self.__typeMap[unicode]  :=
        #     a function with calling sequence
        #       addText(elt, item)
        #     and intended function
        #       [ (elt is an et.Element) and
        #         (item is a str or unicode instance) ->
        #           if elt has no children and elt.text is None ->
        #             elt.text  :=  item
        #           else if elt has no children ->
        #             elt.text  +:=  item
        #           else if elt's last child has .text==None ->
        #             that child's .text  :=  item
        #           else ->
        #             that child's .text  +:=  item ]
        def addText(elt, item):
            if len(elt):
                elt[-1].tail  =  (elt[-1].tail or "") + item
            else:
                elt.text  =  (elt.text or "") + item
        self.__typeMap[str]  =  self.__typeMap[unicode]  =  addText
        #-- 3 --
        # [ self.__typeMap[str], self.__typeMap[unicode]  :=
        #     a function with calling sequence
        #       addInt(elt, item)
        #     and intended function
        #       [ (elt is an et.Element) and
        #         (item is an int instance) ->
        #           if elt has no children and elt.text is None ->
        #             elt.text  :=  str(item)
        #           else if elt has no children ->
        #             elt.text  +:=  str(item)
        #           else if elt's last child has .text==None ->
        #             that child's .text  :=  str(item)
        #           else ->
        #             that child's .text  +:=  str(item) ]
        def addInt(elt, item):
            self.__typeMap[str](elt, str(item))
        self.__typeMap[int]  =  addInt
        #-- 4 --
        # [ self.__typeMap[dict]  :=  a function with calling
        #       sequence 
        #         addDict(elt, item)
        #       and intended function
        #         [ (elt is an et.Element) and
        #           (item is a dictionary) ->
        #             elt  :=  elt with an attribute made from
        #                      each key-value pair from item ]
        def addDict(elt, item):
            for key, value in item.items():
                if isinstance(value, basestring):
                    elt.attrib[key]  =  value
                else:
                    elt.attrib[key]  =  str(value)
        self.__typeMap[dict]  =  addDict
        #-- 5 --
        # [ self.__typeMap[type(et.Element instances)]  :=  a
        #       function with calling sequence 
        #         addElt(elt, item)
        #       and intended function
        #         [ (elt and item are et.Element instances) ->
        #             elt  :=  elt with item added as its next
        #                      child element ]
        def addElement(elt, item):
            elt.append(item)
        sample  =  et.Element('sample')
        self.__typeMap[type(sample)]  =  addElement
# - - -   E l e m e n t M a k e r . _ _ c a l l _ _

    def __call__(self, tag, *argList, **attr):
        '''Handle calls to a factory instance.
        '''
        #-- 1 --
        # [ elt  :=  a new et.Element with name (tag) ]
        elt  =  et.Element(tag)
        #-- 2 --
        # [ elt  :=  elt with attributes made from the key-value
        #            pairs in attr ]
        #   else -> I ]
        if attr:
            self.__typeMap[dict](elt, attr)
        #-- 3 --
        # [ if the types of all the members of pos are also
        #   keys in self.__typeMap ->
        #       elt  :=  elt modified as per the corresponding
        #                functions from self.__typeMap
        #   else -> raise TypeError ]
        for arg in argList:
            #-- 3 body --
            # [ if type(arg) is a key in self.__typeMap ->
            #     elt  :=  elt modified as per self.__typeMap[type(arg)]
            #   else -> raise TypeError ]
            self.__handleArg(elt, arg)
        #-- 4 --
        return elt
# - - -   E l e m e n t M a k e r . _ _ h a n d l e A r g

    def __handleArg(self, elt, arg):
        '''Process one positional argument to the factory instance.

          [ (elt is an et.Element) ->
              if type(arg) is a key in self.__typeMap ->
                elt  :=  elt modified as per self.__typeMap[type(arg)]
              else -> raise TypeError ]
        '''
        #-- 1 --
        # [ if arg is callable ->
        #     value  :=  arg()
        #   else ->
        #     value  :=  arg ]
        if callable(arg):
            value  =  arg()
        else:
            value  =  arg
        #-- 2 --
        # [ if type(value) is a key in self.__typeMap ->
        #     elt  :=  elt modified as per self.__typeMap[type(value)]
        #   else -> raise TypeError ]
        try:
            handler  =  self.__typeMap[type(value)]
            handler(elt, value)
        except KeyError:
            raise TypeError("Invalid argument type: %r" % value)
# - - -   E l e m e n t M a k e r . _ _ g e t a t t r _ _

    def __getattr__(self, tag):
        '''Handle arbitrary method calls.

          [ tag is a string ->
              return a new et.Element instance whose name
              is (tag), and elements of p and kw have
              the same effects as E(*(p[1:]), **kw) ]
        '''
        return partial(self, tag)
# - - - - -   m a i n

E  =  ElementMaker()
