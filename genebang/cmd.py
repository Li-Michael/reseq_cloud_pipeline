#!/usr/bin/env python
#coding:utf-8

import sys
import os
from jsonio import jsonIO
from ConfigParser import ConfigParser
import argparse

__author__='Li Michael'
__version__ = "v 0.1"


class Bio_exec(jsonIO.JsonIO):
    def __init__(self, prog):
        self.prog = prog
        self.cmd = None
        self.section = None
        self.option = None
        self.args = None

        self.cfgfile = None
        self.input = None
        self.output = {'output':None}

    def set_input(self, s_json):
        self.input = s_json
    
    def set_prog(self, prog):
        self.prog = prog

    def set_cmd(self, cmd):
        self.cmd = cmd
    
    def set_section(self, section):
        self.section = section

    def set_option(self, option):
        self.option = option

    def set_args(self, args):
        self.args = args

    def set_cfgfile(self, cfgfile):
        self.cfgfile = cfgfile

    def parseJson(self, s_input, key=None, encoding=None):
        # self.getInput(self, s_json)
        # return the dict
        #return self.json2py(s_input, encoding=encoding)  
        return self.get_value(s_input, key=key, encoding=encoding) 

    def getConfig(self, configfile, section=None):
        kvs = {}
        conf = ConfigParser()
        conf.read(configfile)
        for sections in conf.sections():
            kvs[sections] = conf.items(sections)
        return kvs

    def command(self, input_json, configfile, key_input=None, encoding=None,sections={'Section1':'-', 'Section2':'--'}, sep=' ', **kw):
        input_dict = self.parseJson(input_json, key=key_input, encoding=encoding)
        print input_dict 
        conf = ConfigParser()
        conf.read(configfile)
        print 11
        print self.prog        
        #sections = {'Section1':'-', 'Section2':'--'}
        print sections
        if kw == {}:
            cmd1 = ' '.join([self.prog, conf.get('CMD','cmd')])
            for key,values in sections.items():
                cmd2 = ' '.join(map(lambda i: values+i[0]+sep+i[1],conf.items(key)) )
        cmd = cmd1 + ' ' + cmd2
        return cmd

    def write(self, s_input, key=None, encoding=None):
        pass    


