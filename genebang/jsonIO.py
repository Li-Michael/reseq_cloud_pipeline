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
import demjson,json
#import pandas

#f1 = sys.argv[1]
"""
json2py decode the json object to python object
"""
def json2py(s, encode=None): # encode='utf-8'
    if os.path.isfile(s):
        return demjson.decode_file(s, encoding=encode)
    else:
        return demjson.decode(s, encoding=encode)

def py2json(s, encode=None, compact=False):
    try:
        return demjson.encode(s, encoding=encode, compactly=compact)
    except:
        os.stderr.write("Check the encode object!")
        sys.exit(1)



