import jsonIO
a = jsonIO.json2py("test.json")
a
#{u'username': u'loleina', u'age': 16, u'type': [u'dic1', 1, 4.5], u'wang': u'http:\\www.baidu.com'}
jsonIO.py2json(a)
#u'{ \n  "age" : 16,\n  "type" : [ \n      "dic1",\n      1,\n      4.5\n    ],\n  "username" : "loleina",\n  "wang" : "http:\\\\www.baidu.com"\n}\n'
print jsonIO.py2json(a)
"""
{ 
    "age" : 16,
    "type" : [ 
        "dic1",
        1,
        4.5
    ],
    "username" : "loleina",
    "wang" : "http:\\www.baidu.com"
}
"""

a['wang']
#u'http:\\www.baidu.com'
print a['wang']
#u'http:\www.baidu.com'
print repr(a['wang'])
#u'http:\\www.baidu.com'


