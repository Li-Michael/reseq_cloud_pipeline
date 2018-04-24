#!/usr/bin/env python
#coding:utf-8
"""
-------------Bio_cmd------------------
1. 确定json结构
2. 按json结构配置软件的configfile
3. 运行该脚本即可
--------------------------------------
"""

import cmd

test = cmd.Bio_cmd('SOAPnuke')
test.write('input.json', 'SOAPnuke.cfg', key_input='input', key_samples='rawdata')

