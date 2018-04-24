#!/usr/bin/env python
#-*-coding:utf-8-*-

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
        self.option = '' 
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

    def configfile_cmd(self, configfile, key_input=None, encoding=None, sections={'Section1':'-', 'Section2':'--'}, sep=' ', **kw):
        """
        根据cofigfile文件创建cmd
    	"""
        conf = ConfigParser()
        conf.read(configfile)
        #sections = {'Section1':'-', 'Section2':'--'}
        #print [i for i in sections.items()]
        for key,values in sections.items():
            self.option += [' '.join(map(lambda i: values+i[0]+sep+i[1], conf.items(key)) ),]
            
            cmd1 = ' '.join([self.prog, conf.get('CMD', 'cmd')] +  self.option)
            # **kw 用来扩充功能 
            if kw == {}:
                return cmd1
            else:
                return cmd1

    def mkmoduledir(self,path, mode=0755):
        if not os.path.isdir(path):
            os.makedirs(path, mode=mode)
            os.chdir(path)
	
        for subdir in ["jsondir", "output", "report", "shell"]:
            if not os.path.isdir(subdir):
                os.mkdir(subdir)

    def jsonconfig_cmd(self, input_config, key_software=None, encoding=None, sep=' '):
        """
    	根据json_config生成cmd
        """
    	config_dict = input_config[key_software]
        cmd1 = config_dict.pop('cmd')
        self.option = sep+' '.join([ key+sep+value for key,value in config_dict.items() ])
        cmd1  += self.option
        return cmd1
    
    # 用来按sample写 .sh 文件
    def write(self, input_json, configfile=None, key_input=None, key_samples=None, key_software=None, suffix=None, encoding=None, sep=' ', IOinput={'input':[], 'output':[]}, sections={'Section1':'-', 'Section2':'--'}, **kw):
        input_dict = self.parseJson(input_json, encoding=encoding)
        if configfile:
            cmd1 = self.configfile_cmd(configfile, key_input=key_input, encoding=encoding, sections=sections, sep=sep, kw=kw)
        else:
            cmd1 = self.jsonconfig_cmd(input_dict['config'], key_software=key_software, sep=sep)
        
        samples = input_dict[key_input][key_samples]
        input_dict.pop(key_input)
		
        workspace = input_dict['output']['workspace']
        #print workspace
        self.mkmoduledir(workspace)
        currdir= os.getcwd()
        print("current dir:"+currdir)	
        
        # 按sample生成 .sh  { sample1:{ 'Lan1':[] } }  
        for key,value in samples.items():
            sample_path = os.path.join(workspace,'output', key, value.keys()[0])
            print sample_path
            if not os.path.isdir(sample_path):
                os.makedirs(sample_path)
			
		# 设置input 
                prefix = key + "." +value.keys()[0]
                sample = value.values()[0]
                
                if (len(sample) == len(IOinput['input'])) and (len(IOinput['input']) > 1):
                    full_cmd = cmd1 + ' ' + ' '.join([ IOinput['input'][i]+sep+sample[i] for i in range(len(sample)) ])
                elif len(sample) > len(IOinput['input']) and len(IOinput['input']) == 1:
                    full_cmd = cmd1 + ' ' + ' '.join([ IOinput["input"][0]+sep+i for i in sample ])
                else:
                    sys.stderr.write("[ERROR] Check the parameter: IOinput\n")
                    sys.exit(1)
                    
                # 设置output,  samplename的问题
                if suffix:
                    if len(sample) == len(IOinput['output']) and len(IOinput['output'])>1:
                        full_cmd += ' ' + ' '.join([ IOinput['output'][i] + sep + os.path.join(sample_path,prefix+'_'+str(i+1)+'.'+suffix) for i in range(len(IOinput['output'])) ])
                    elif len(sample) > len(IOinput['output']) and len(IOinput['output']) == 1:
                        full_cmd += ' ' +  IOinput['output'][0] + sep + os.path.join(sample_path,prefix+'.'+suffix)
                    else: 
                        sys.stderr.write("[ERROR] Check the sample's numbers!\n")
                        sys.exit(1)
                        
                    os.chdir(os.path.join(currdir,'shell'))
                    suffix_file = os.getcwd()
                    with open(os.path.join(suffix_file, prefix+'.'+self.prog+'.sh'), 'w') as f:
                        f.write(full_cmd + "\n")
			

    def sampleParse(self, input_json, key="input", encoding=None):
        """
        parse the sample dir from the json, and mkdir
        """
        return parseJson(input_json, key=key, encoding=encoding).values()
		
    #def sampledir(path)
