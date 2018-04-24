#!/usr/bin/env python
#coding:utf-8
"""
===========Performs the following translations in decoding by default:
    -JSON-          -Python-
    object	    dict
    array	    list
    string	    unicode
    number(int)	    int, long
    number(real)    float
    true	    True
    false	    False
    null	    None

=========Supports the following objects and types by default: encoding
    -Python-	    -JSON-
    dict	    object
    list, tuple	    array
    str, unicode    string
    int,long,float  number
    True	    true
    False	    false
    None	    null
============================================================
"""

import sys,os
import demjson  #,json
#import pandas

#f1 = sys.argv[1]
"""
json2py decode the json object to python object
"""
class JsonIO(demjson.JSON):
    def __init__(self):
        self.s = None
        
    def json2py(self, s, encoding=None): # encode='utf-8'
        if os.path.isfile(s):
            return demjson.decode_file(s, encoding=encoding)
        else:
            return demjson.decode(s, encoding=encoding)

    def py2json(self, s, encoding=None, compact=False):
        try:
            return demjson.encode(s, encoding=encoding, compactly=compact)
        except:
            os.stderr.write("Check the encode object!\n")
            sys.exit(1)

    def get_value(self,s, key=None,encoding=None):
        values = self.json2py(s, encoding)
        if key != None:
            value = values[key]
        else:
            value = values
        return value


