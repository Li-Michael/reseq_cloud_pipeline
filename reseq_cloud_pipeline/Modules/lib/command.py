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

	def cfgfile_cmd(self, cfgfile=None, key_input=None, encoding=None, sections={'Section1':'-', 'Section2':'--'}, sep=' ', **kw):
		"""
		根据cofigfile文件创建cmd
		"""
		if cfgfile:
			conf = ConfigParser()
			conf.read(cfgfile)
			#sections = {'Section1':'-', 'Section2':'--'}
			#print [i for i in sections.items()]
			for key,values in sections.items():
				self.option += [' '.join(map(lambda i: values+i[0]+sep+i[1], conf.items(key)) ),]
		
			cfg_cmd = ' '.join([self.prog, conf.get('CMD', 'cmd')] +  self.option)
        
		else:
			cfg_cmd = ' '
		# **kw 用来扩充功能 
		if kw == {}:
			return cfg_cmd
		else:
			return cfg_cmd


	def modulemkdir(self, mode=0755, **output):
		"""
		mkdir the workspace and return the workspace dirpath dict
		"""
		if "workspace" in output:
			workdir = output["workspace"]
			self.workmkdir(workdir, mode=mode)
			workspace = {"jsondir":workdir+"jsondir", "outdir":workdir+"outdir", "report":workdir+"report", "shell":workdir+"shell"}
		else:
			for subdir in [ output["jsondir"], output["outdir"], output["report"], output["shell"] ]:
				if not os.path.isdir(subdir):
					os.mkdirs(subdir, mode=mode)
			workspace = {"jsondir":output["jsondir"]+"jsondir", "outdir":output["outdir"]+"outdir", "report":output["report"]+"report", "shell":output["shell"]+"shell"}
		return workspace

	def sampleParse(self, **samples):
		"""
		parse the sample dir from the json, and mkdir
		return samples dict : {"sample1.Lane1":["/path/fq1_1.fq.gz", "/path/fq1_2.fq.gz"]}
		"""
		sample_path = {}
		for key,value in samples.items():
			if isinstance(value, dict):
				for subkey, subvalue in value.items():
					sample_path[key+"."+subkey] = subvalue 
			else:
				sample_path[key] = value
		return sample_path
			
	
	def jsoncfg_cmd(self, cfg_json=None, key_software=None, encoding=None, sep=' ', cmd=[]):
		"""
		根据json config生成cmd
		"""
		main = cfg_json['main']
		project_id = main['project_id']

		software_dict = cfg_json['software'][key_software]
		cmd1 = software_dict.pop('cmd')
		version = software_dict.pop('version')
		self.option = sep+' '.join([ key+sep+value  if not value in [True,False] else key+sep  for key,value in software_dict.items() ])
		cmd1  += self.option
		return cmd1
   
	
	def fullCmd(self, subcmd=None, outdir=None, suffix=None, sep=' ', others='', IOopt={'input':[], 'output':[], 'outdir':None}, sample_dict={}, **kw):
		
		"""
		json_cmd	-> the jsonfile command
		config_cmd	-> the command from the configure file that could be parsed by Module CofigParser
		prefix		-> as a prefix for generating .sh files
		suffix		-> as a suffix for the output name
		sep			-> connection character between options and parameters
		IOopt		-> input/output: the input/output options of a software
		**kw		-> maybe other options
		"""
		outname, sample = sample_dict.keys()[0], sample_dict.values()[0]
		
		# 按sample生成 .sh  { sample1.Lane1:[fq1_1.fq.gz, fq1_2.fq.gz] }  
		# 设置input 
		if (len(sample) == len(IOopt['input'])) and (len(IOopt['input']) > 1):
			cmd = subcmd + ' ' + ' '.join([ IOopt['input'][i]+sep+sample[i] for i in range(len(sample)) ])
		elif len(sample) > len(IOopt['input']) and len(IOopt['input']) == 1:
			cmd = subcmd + ' ' + ' '.join([ IOopt["input"][0]+sep+i for i in sample ])
		else:
			sys.stderr.write("[ERROR] Check the parameter: IOoptions\n")
			sys.exit(1)
	
		# 设置output,  samplename的问题
		if IOopt['outdir'] or (IOopt['outdir'] !=''):
			if len(sample) == len(IOopt['output']) and len(IOopt['output'])>1:
				cmd += ' ' + IOopt['outdir'] +sep+ outdir +' '+ ' '.join([ IOopt['output'][i]+sep+ outname+'_'+str(i+1)+'.'+suffix for i in range(len(IOopt['output'])) ])
			elif len(sample) > len(IOopt['output']) and len(IOopt['output']) == 1:
				cmd += ' ' + IOopt['outdir'] +sep+ outdir +' '+ IOopt['output'][0] + sep + outname+'.'+suffix
			else: 
				sys.stderr.write("[ERROR] Check the sample's numbers!\n")
				sys.exit(1)
		else:
			if len(sample) == len(IOopt['output']) and len(IOopt['output'])>1:
				cmd += ' ' + ' '.join([ IOopt['output'][i]+sep+ os.path.join(outdir,outname+'_'+str(i+1)+'.'+suffix) for i in range(len(IOopt['output'])) ])
			elif len(sample) > len(IOopt['output']) and len(IOopt['output']) == 1:
				cmd += ' ' +  IOopt['output'][0] + sep + os.path.join(outdir, outname+'.'+suffix)
			else: 
				sys.stderr.write("[ERROR] Check the sample's numbers!\n")
				sys.exit(1)

		return cmd +' '+ other 


	# 用来按sample写 .sh 文件
	def cmd(self, cfg_json=None, cfgfile=None, key_input=None, key_samples=None, key_config='config', key_software=None, prefix=None, suffix=None, encoding=None, sep=' ', others='', IOopt={'input':[], 'output':[], 'outdir':None}, sections={'Section1':'-', 'Section2':'--'}, **kw):
		"""
		cfg_json	-> the json config file
		cfgfile	-> the configure file that could be parsed by Module CofigParser
		key_input	-> as the input keyword in json
		key_samples	-> as the input samples keyword in json
		key_config	-> as the configure keyword in json
		key_software	-> ad the software configure keyword in json
		prefix		-> as a prefix for generating .sh files
		suffix		-> as a suffix for the output name
		encoding	-> character encoding type
		sep			-> connection character between options and parameters
		IOinput		-> input/output: the input/output options of a software
		sections	-> the prefix characters of options in configfile 
		**kw		-> maybe other options
		"""
		input_dict = self.parseJson(cfg_json, encoding=encoding)
		config_cmd = self.cfgfile_cmd(cfgfile=cfgfile, key_input=key_input, encoding=encoding, sections=sections, sep=sep, kw=kw)
		cmd_json = self.jsoncfg_cmd(cfg_json=input_dict[key_config], key_software=key_software, sep=sep)
		cmd = cmd_json + " " + config_cmd

		samples = input_dict[key_input][key_samples]
		#input_dict.pop(key_input)

		workspace = self.modulemkdir(input_dict['output'])
		samples = self.sampleParse(samples)

		currdir= os.getcwd()
		sys.stderr.wirte("[INFO] Current directory: "+currdir+"\n")	
		
		# 按sample生成 .sh  { sample1.Lane1:[fq1_1.fq.gz, fq1_2.fq.gz] }  
		for key,sample in samples.items():
			sample_path = os.path.join(workspace["outdir"], key.replace(r".", r"/"))
			print sample_path
			if not os.path.isdir(sample_path):
				os.makedirs(sample_path)
			 
			#def fullCmd(self, subcmd, outdir, suffix, sep=' ', others='', IOopt={'input':[], 'output':[], 'outdir':None}, sample={}, **kw):
			cmd = fullCmd(subcmd=cmd, outdir=sample_path, suffix=suffix, sep=sep, others=others, IOopt=IOopt, sample_dict={key:sample}, **kw)

			shname = '.'.join(prefix, key, suffix, 'sh')
			filename = os.path.join(workspace["shell"], shname)
			with open(filename, 'w') as f:
				f.write(cmd + " && \\ \ntouch %s.ok\n" %shname)
			sys.stderr.write("[INFO] "+ filename + "is ready!\n")	

