#!/usr/bin/env python
#coding:utf-8

import sys
import os
from jsonio import jsonIO
from ConfigParser import ConfigParser
import argparse

__author__='Li-Michael  lizhenzhong@basepedia.com'
__version__ = "v 0.1"


class Bio_cmd(jsonIO.JsonIO):
    def __init__(self, prog):
        self.prog = prog
        self.cmd = None
        self.section = None
        self.option = [] 
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

    def command(self, input_sample, configfile, key_input=None, encoding=None, sections={'Section1':'-', 'Section2':'--'}, sep=' ', **kw):
        #input_dict = self.parseJson(input_json, key=key_input, encoding=encoding)
        conf = ConfigParser()
        conf.read(configfile)
        #sections = {'Section1':'-', 'Section2':'--'}
        print [i for i in sections.items()]
        for key,values in sections.items():
            self.option += [' '.join(map(lambda i: values+i[0]+sep+i[1], conf.items(key)) ),]
        
        cmd1 = ' '.join([self.prog, conf.get('CMD', 'cmd')] +  self.option)
        
        # **kw 用来扩充功能 
        if kw == {}:
            return cmd1
        else:
            return cmd1
    
    # 用来按sample写 .sh 文件
    def write(self, input_json, configfile, key_input=None, key_samples=None, encoding=None, sections={'Section1':'-', 'Section2':'--'}, sep=' ', **kw):
        cmd1 = self.command(input_json, configfile, key_input=key_input, encoding=encoding, sections=sections, sep=sep, kw=kw)
        input_dict = self.parseJson(input_json, key=key_input, encoding=encoding)
        samples = input_dict[key_samples]
        input_dict.pop(key_samples)
        
        # 按sample生成 .sh
        for key in samples:
            if len(samples[key]) == 2:
                full_cmd = cmd1.format(sample=samples[key], ref=input_dict) 
            elif len(samples[key]) == 1:
                full_cmd = cmd1.format(sample=samples[key], ref=input_dict)
            else: 
                sys.stderr.write("[ERROR] Check the sample's numbers!\n")
                sys.exit(1)
            
            # 存在样品名的问题
            #prefix = samples[key][0].split('.')[0]
            prefix = key
            with open(prefix+'.'+self.prog+'.sh', 'w') as f:
                f.write(full_cmd + "\n")



