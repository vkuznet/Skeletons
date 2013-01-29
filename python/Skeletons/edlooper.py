#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable-msg=

"""
File       : edlooper.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description: generates EDLooper CMSSW infrastructure
"""

# system modules
import sys

# package modules
from Skeletons.pkg import AbstractPkg

class EDLooper(AbstractPkg):
    "EDLooper implementation of AbstractPkg"
    def __init__(self, config=None):
        if  not config:
            config = {}
        AbstractPkg.__init__(self, config)
        
    def cpp_files(self, kwds):
        "Generate C++ files"
        args = self.config.get('args', None)
        if  not args:
            args  = {'__datatypes__': ['MyData']}
        kwds.update(args)
        return super(EDLooper, self).cpp_files(kwds)
