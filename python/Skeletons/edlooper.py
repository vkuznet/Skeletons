#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable-msg=

"""
File       : edlooper.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description: generates EDLooper CMSSW infrastructure
"""

# system modules
import os
import sys

# package modules
from Skeletons.pkg import AbstractPkg

class EDLooper(AbstractPkg):
    "EDLooper implementation of AbstractPkg"
    def __init__(self, config=None):
        if  not config:
            config = {}
        dirs = ['doc', 'plugins', 'python', 'test']
        config.update({'dirs':dirs})
        AbstractPkg.__init__(self, config)
        
    def cpp_files(self, kwds):
        "Generate C++ files"
        args = self.config.get('args', None)
        if  not args:
            args  = {'__datatypes__': ['MyData']}
        kwds.update(args)
        if  not kwds.has_key('cpp_dir'):
            kwds.update({'cpp_dir':'plugins'}) # location of cpp files
        else: # call within SubSystem/Package/plugins area
            kwds.update({'__pkgname__': os.getcwd().split('/')[-2]})
        return super(EDLooper, self).cpp_files(kwds)
